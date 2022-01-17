#!/usr/bin/env python

import rospy
import smach
import numpy as np
import actionlib
import math
import tf
import sys, os

from threading import Thread
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from communication import server_tcp


# Thread in order to detect tcp orders
class conexion(Thread):

    done = False

    def __init__(self):
        super(conexion, self).__init__()
        self.daemon = True
        self.key = ""

        self.server = server_tcp(12343) # tcp server

        self.start() # Execute run() 

    # Wait for android apk message
    def run(self):
        while not self.done and self.server.connected:
            self.key = self.server.recibir()

    # Close thread
    def stop(self):
        self.done = True
        self.join(1)
       

app = conexion()


# Deafault class where needed functions are defined
# State classes are inherited of this
class default(smach.State):

    transitions = {
        '\x03': 'exit',
        'E': 'exit',
        'W': 'WAIT',
        'F': 'FOLLOW',
        'R': 'RECORD',
        'P': 'PATH',
        'N': 'NPATH',
        'H': 'GOHOME',
        'S': 'SETHOME',
        'T': 'TELEOP'
    }

    def __init__(self):
        smach.State.__init__(self, outcomes=self.transitions.keys(), input_keys=['input_1','input_2'], output_keys=['output_1','output_2'])
        # Subscribe to robot laser scan
        self.sub = rospy.Subscriber('/scan', LaserScan, self.clbk_laser)
        self.dist = 0
        self.alpha = 0

        # Listen to tf data
        self.listener = tf.TransformListener()
        self.rate = rospy.Rate(10.0)

        # Initialize values
        self.trans = 0, 0, 0
        self.prev_trans = self.trans
        self.recorded_path = []
        self.home = ()

        # Create ROS client for the action
        self.client =  actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
         
        # Inicializamos el estado como Wait.
        self.key = 'W'
        self.tele_speed = 0
        self.tele_angle = 0
        self.last_state = self.key

        # Velocity publisher
        self.msg = Twist()
        # self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)

        # Stop robot once finished execution
        rospy.on_shutdown(self.stop_robot)

    # Get current position of the robot on the map
    def getCurrentPos(self):
        self.trans,_ = self.listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        position = round(self.trans[0],3), round(self.trans[1],3) # Tuple
        return position

    # Closest point from a point to an array of points
    def closest_path_point(self, pos, path_points):
        distances = np.sqrt(np.sum((path_points - pos)**2, axis=1))

        temp = distances.argmin()
        if temp < 0 or temp >= len(distances):
            print(temp)
            
        return tuple(path_points[temp])

    # Move robot to a given point
    def move_To(self, target_point, next_after_target):

        # Objective point
        goal = MoveBaseGoal() # Type
        goal.target_pose.header.frame_id = "map" # Reference
        goal.target_pose.pose.position.x = target_point[0]   
        goal.target_pose.pose.position.y = target_point[1]
        
        # Get orientation to next point
        dx = next_after_target[0] - target_point[0]
        dy = next_after_target[1] - target_point[1]
        goal_angle = math.atan2(dy,dx)
        RPY = (0,0,goal_angle)  
        Q = quaternion_from_euler(*RPY)

        # Fix some quaternion components
        goal.target_pose.pose.orientation.z = Q[2]
        goal.target_pose.pose.orientation.w = Q[3]


        self.client.send_goal(goal) # Send objective point

    # Follow saved path
    def execute_path(self):
        # If path is not saved or has one only point return to Wait state
        if len(self.recorded_path) > 1:

            # When entering this state from another state, assign target point to the closest point from current point to the path points
            if self.last_state != self.key:
                target_point = self.closest_path_point(self.getCurrentPos(), np.array(self.recorded_path))
                self.next_target = target_point
            
            # Reassign target point to next point in the path, after the current target point
            if (self.client.get_state() is not GoalStatus.ACTIVE) and (self.client.get_state() is not GoalStatus.PENDING):

                idx = self.recorded_path.index(self.next_target)
                idx = idx+1 if idx+1 < len(self.recorded_path) else 0
                self.move_To(self.next_target, self.recorded_path[idx])

                self.next_target = self.recorded_path[idx]   # Update next point on path
                
            self.last_state = self.key

            return True

        elif len(self.recorded_path) == 1:
            print('\033[93m'+"There is not a path, just one point is saved"+'\033[0m')
            self.key = "W"
        else:
            print('\033[93m'+"Path not already saved"+'\033[0m')
            self.key = "W"

        return False

    # Save points once robot is moved a certain distance
    def record_path(self, diff, userdata):
        position = self.getCurrentPos()

        distance = math.sqrt((self.trans[0] - self.prev_trans[0])**2+(self.trans[1] - self.prev_trans[1])**2) # Moved distance
        if distance > diff:
            self.recorded_path.append(position) # Save position
            userdata.output_1 = self.recorded_path
            self.prev_trans = self.trans # Update 
            sys.stdout.write(".") # Execution feedback
            sys.stdout.flush()        

    # Remove current saved path
    def forget_path(self,userdata):
        self.recorded_path = []
        userdata.output_1 = self.recorded_path
        print('\033[32m'+"Path has been forgotten"+'\033[0m')
        self.key = 'W'

    # Extract laser data of the closest object
    def clbk_laser(self, msg):
        ranges = np.array(msg.ranges) # Range laser data
        ranges = ranges[::-1]

        ranges[np.isnan(ranges) + np.isinf(ranges)] = 10.0 # Change NaN and infinite values

        size = int(len(ranges))/6
        ranges = ranges[size:5*size]
        size = int(len(ranges)/3)
        ranges = ranges[size:2*size]
        size = int(len(ranges))/2

        self.range = size
        self.alpha = (np.argmin(ranges) - size) # Angle of the closest object
        self.dist = ranges[np.argmin(ranges)] # Distance of the closest object

    # Move robot following the closest object
    def take_action(self):
        # Initial speed
        linear_speed = 0
        angular_speed = 0
        min_dist = 0.4
        max_dist = 1.0 

        # Change velocities depending on closest object position, avoiding collide with it
        if (min_dist < self.dist <= max_dist) and self.range == 106:
            linear_speed = (self.dist/max_dist)*0.4
            angular_speed = (self.alpha/106.0)*1.5

        # Publish velocities
            self.msg.linear.x =  linear_speed
            self.msg.angular.z = angular_speed
            self.pub.publish(self.msg)

    # Set velocities to 0 and publish them
    def stop_robot(self):
        self.msg.linear.x  = 0
        self.msg.angular.z = 0
        self.pub.publish(self.msg) 

    # Move robot to home position.
    def go_home(self):
        if len(self.home):
            if (self.client.get_state() is not GoalStatus.ACTIVE) and (self.client.get_state() is not GoalStatus.PENDING):
            
                # Objective point.
                goal = MoveBaseGoal() # Type
                goal.target_pose.header.frame_id = "map" # Reference
                goal.target_pose.pose.position.x = self.home[0]
                goal.target_pose.pose.position.y = self.home[1]


                # Fix some quaternion components.
                Q = self.home[2]
                goal.target_pose.pose.orientation.z = Q[2]
                goal.target_pose.pose.orientation.w = Q[3]

                self.client.send_goal(goal) # Send objective point

            if self.client.get_state() is GoalStatus.SUCCEEDED:
                print('\033[32m'+"Home achieved"+'\033[0m')
                self.key = 'W'
                return False
            else:
                return True

        else:
            print('\033[93m'+"Home not already set"+'\033[0m')
            self.key = 'W'

        return False

    # Set robot home.
    def set_home(self, userdata):
        pos, quat = self.listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        self.home = pos[0], pos[1], quat

        userdata.output_2 = self.home
        print('\033[32m'+"Set home"+'\033[0m')
        self.key = 'W'

    # Move robot following the closest object
    def teleop_action(self):
        # Initial speed
        max_linear_speed = 0.5
        max_angular_speed = 2
        tele_speed = self.tele_speed
        tele_angle = self.tele_angle

        if tele_speed == 0: 
            tele_angle = 0

        if tele_angle > 180:
            tele_angle -= 360

        linear_speed = (tele_speed/99.0)*max_linear_speed
        angular_speed = (tele_angle/180.0)*max_angular_speed

        # Publish velocities
        self.msg.linear.x =  linear_speed
        self.msg.angular.z = angular_speed
        self.pub.publish(self.msg)



    # Function executed when an state is iniciated
    def execute(self, userdata):

        while True:
            
            temp = app.key.upper()

            if temp:
                self.key = temp[0]
                self.tele_angle = int(temp[1:4])
                self.tele_speed = int(temp[4:])
            else:
                self.key = ""


            if self.key in self.transitions.keys():
                app.key = ""
                break

            if not self.main(userdata): break

            if rospy.is_shutdown():
                self.key = '\x03'
                break
            

        return self.key


    # Function modified in eac class in order to execute needed functions
    def main(self, userdata): 
        # Update shared data
        self.recorded_path = userdata.input_1
        userdata.output_1 = self.recorded_path

        self.home = userdata.input_2
        userdata.output_2 = self.home



# State: Stop robot
class Wait(default):

    def __init__(self):
        default.__init__(self)

    def main(self,userdata):
        default.main(self,userdata)
        default.stop_robot(self)

        return True

# State: Follow person      
class Follow(default):
    def __init__(self):
        default.__init__(self)

    def main(self,userdata):
        default.main(self,userdata)
        self.take_action()
        return True

# State: Follow person and save path
class Record(default):
    def __init__(self):
        
        default.__init__(self)

    def main(self, userdata):
        default.main(self, userdata)
        try:
            self.take_action()
            self.record_path(0.5, userdata)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            pass

        return True

# State: Execute recorded path
class Path(default):
    def __init__(self):
        default.__init__(self)

    def main(self,userdata):
        default.main(self,userdata)
        return self.execute_path()

# State: Forget saved path
class NPath(default):
    def __init__(self):
        default.__init__(self)
    
    def main(self,userdata):
        default.main(self,userdata)

        self.forget_path(userdata)

        return False

# State: Go to point selected as "Home"
class GoHome(default):
    def __init__(self):
        default.__init__(self)
    
    def main(self,userdata):
        default.main(self,userdata)

        return self.go_home()

# State: Select current position as "Home"
class SetHome(default):
    def __init__(self):
        default.__init__(self)
    
    def main(self,userdata):
        default.main(self,userdata)

        self.set_home(userdata)

        return False

# State: Joystick control
class Teleop(default):
    def __init__(self):
        default.__init__(self)

    def main(self,userdata):
        default.main(self,userdata)
        self.teleop_action()
        return True





def main():
    rospy.init_node('smach_state_machine')

    # SMACH state machine
    if app.server.connected:
        sys.stdout = open(os.devnull, 'w')  # Deactivate terminal prints
        sm = smach.StateMachine(outcomes=['exit']) # Define state machine object
        
        sm.userdata.path = [] # Data shared between states
        sm.userdata.home = () # Data shared between states
        
        io = {  'input_1':'path','input_2':'home',
                'output_1':'path','output_2':'home' }

        # States and transitions
        with sm:
            smach.StateMachine.add('WAIT', Wait(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('FOLLOW', Follow(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('RECORD', Record(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('PATH', Path(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('NPATH', NPath(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('GOHOME', GoHome(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('SETHOME', SetHome(), transitions=default.transitions, remapping=io)
            smach.StateMachine.add('TELEOP', Teleop(), transitions=default.transitions, remapping=io)


        # Execute SMACH plan
        sys.stdout = sys.__stdout__ # Reactivate terminal prints
        sm.execute() # Start state machine

    app.stop() # Close thread


if __name__ == '__main__':
    main()
