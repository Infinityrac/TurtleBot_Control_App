# TURTLEBOT CONTROL APP

<p align="center">
  <img src="doc/Portada.jpg" alt="animated"/>
</p>

## INDEX:
  
  - [1. Introduction](#p1)
  - [2. Environments](#p2)  
  - [2.1. Simulated Environment](#p2.1) 
  - [2.2. Real Environment](#p2.2)  
  - [3. Video](#p3)  
  - [4. Credits](#p4)  


## Introduction:

This is the final project of 4º Robotic Engineering at University of Alicante for the subject Mobile Robots. Different codes have been developed in `Python` so that a `TurtleBot` can do some tasks. This task are:

  - Person following
  - Save/Delete path
  - Execute path
  - Set/Delete home
  - Go home
  - Joystick control

To execute one task or another, an `Android app` is used. This app connect with the robot and send information using TCP. 
Code is estructured through a SMACH state machine. When the app send a message to the robot, code check if it is valid and change its state.

## Work environments: <a name="p2"/>

Not always real robot can be used, two versions have been created:
  - ROS Noetic simulation
  - Real TurtleBot control
    
  ### - Simulated environment: <a name="p2.1"/>
   
  Simulated environment has been coded with `Python3` on `ROS Noetic`. First of all, open Gazebo simulator, in this case, ROS defalut house map is used. On one terminal execute following commands:

    export TURTLEBOT3_MODEL=waffle
    roslaunch turtlebot3_gazebo turtlebot3_house.launch

  Open new terminal and execute navigation module (is is necessary to have previosly mapped the area):
  
    export TURTLEBOT3_MODEL=waffle
    roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/house.yaml
  _Note: Both files (`.yaml` and `.pgm`) must be on `HOME` directory._
   
  This will open a rviz window where robot, map and localization point cloud can be seen. Use 2D POSE ESTIMATE to estimate the current position of the robot in the map.
  
  Execute code `main.py` and the `Android app`. TCP conexion uses `port:12343`


  ### - Real Environment: <a name="p2.2"/>
  
  Real environment has been coded using `Python 2` on `ROS Kinetic`
  Para el entorno real, se ha programado con `Python 2` en `ROS Kinetic`. Para poder trabajar en este entorno, primero de todo es neceario inicializar el Turtlebot real. Para ello ejecutamos los siguientes dos comandos en terminales distintas.

    roslaunch turtlebot_bringup minimal.launch
    roslaunch turtlebot_bringup hokuyo_ust101x.launch
    
  Tras esto, abrimos un nuev terminal y ejecutamos los siguientes comandos para iniciar el módulo de navegacion:
  
    export TURTLEBOT_3D_SENSOR=astra
    roslaunch turtlebot_navigation amcl_demo.launch map_file:=$HOME/house.yaml
   _Nota: Ambos ficheros del mapa (`.yaml` y `.pgm`) deben estar en el directorio `HOME`._
    
  Tras esto, será neceario abrir una ventana de `rviz` desde un ordenador remoto. Para ello ejecutaremos el fichero `setvars.bash` y abriremos una nueva terminal. Desde esta, ejecutaremos el siguiente comando.
  
    rosrun rviz rviz
    
  Con esto, se nos abrirá `rviz` y ya solo será necesario añadir los módulos correspondientes para que se muestre el mapa, la nube de puntos y el robot. Una vez hecho esto, ya solo queda ejecutar el programa `main.py` y la app android. La conexión es mediante tcp desde el `puerto: 12343`.

## Video del funcionamiento: <a name="p3"/>

Si hacemos click en el gif, podremos ver un vídeo del funcionamiento del proyecto.

<p align="center">
  <a href="https://youtu.be/j-LswYOt--s">
    <img src="doc/clip.gif" alt="animated"/>
  </a>
</p>

## Creditos: <a name="p4"/>

Proyecto realizado por:

  - Adrián Sanchis Reig
  - Rafael Antón Cabrera
  - Andrés Gómez-Caraballo Yélamos


