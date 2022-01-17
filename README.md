# TURTLEBOT CONTROL APP

Esto es el trabajo final de ingeniería Robótica en la Universidad de Alicante para la asignatura de Robots Móviles. En este, se han desarrollado distintos códigos en `Python 2` para que un `Turtlebot` pueda resolver una serie de tareas. Estas tareas son:

  - Seguimiento de personas.
  - Grabar/Olvidar rutas.
  - Reproductor de rutas.
  - Establecer/Olvidar home.
  - Ir al home.
  - Control mediante Joystick.

Para ejecutar una tarea u otra, se hace uso de una `aplicación android` desde la cual podemos conectarnos y enviarle por tcp las tareas que queremos que realice. Todo esto está estructurado dentro de la máquina de estados Smach. De forma que cada vez que la app envía un mensaje al Turtlebot, este comprueba si el mesaje es válido y cambia al estado indicado en el mensaje.

## Entornos de trabajo:

Puesto que no siempore se ha tenido acceso al robot, se han creado dos versiones. Una en `Python 2` que permite controlar a un Turtlebot real y otra en `Python 3`, hecha en `ROS Noetic` desde la que es posible controlar una simulacion en Gazebo:
    
  ### - Entorno Simulado:
   
  Para el entorno simulado, se ha programado con `Python 3` en `ROS Noetic`. Para poder trabajar en este entorno, primero de todo es neceario abrir el simulador de Gazebo con un mapa ya creado. Para ello se ha hecho uso del mapa house por defecto. Para ello creamos los siguientes dos comandos en un terminal.

    export TURTLEBOT3_MODEL=waffle
    roslaunch turtlebot3_gazebo turtlebot3_house.launch

  Tras esto, abrimos un nuev terminal y ejecutamos los siguientes comandos para iniciar el módulo de navegacion:
  
    export TURTLEBOT3_MODEL=waffle
    roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/house.yaml
  _Nota: Ambos ficheros del mapa (`.yaml` y `.pgm`) deben estar en el directorio `HOME`._
    
  Esto nos abrirá además una ventana de `rviz` desde la que podremos visualizar el robot, el mapa y la nube de puntos que representa las posibles posiciones del robot. Seleccionando la opción de `2D POSE ESTIMATE` y haciendo click en el mapa en la posición en la que se encuentra el robot en la simulación haremos que la navegación se ubique entorno a ese punto.
  
  Una vez hecho esto, ya solo queda ejecutar el programa `main.py` y la app android. La conexión es mediante tcp desde el `puerto: 12343`.


  ### - Entorno Real:
  
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

## Video del funcionamiento:

Si hacemos click en el gif, podremos ver un vídeo del funcionamiento del proyecto.

<p align="center">
  <a href="https://youtu.be/j-LswYOt--s">
    <img src="clip.gif" alt="animated"/>
  </a>
</p>

## Creditos:

Proyecto realizado por:

  - Adrián Sanchis Reig
  - Rafael Antón Cabrera
  - Andrés Gómez-Caraballo Yélamos


