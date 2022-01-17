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

Puesto que no siempore se ha dispuesto


## Video del funcionamiento:

<p align="center">
  <a href="https://youtu.be/j-LswYOt--s">
    <img src="clip.gif" alt="animated"/>
  </a>
</p>

## Instalacion:

- Seguir testeando con MediaPipe.
- Ver si utilizar la Z que proporciona es factible para la profundidad. (Parece que si pero no es suficiente)
- Probar a obtener las coordenaadas articulares y pasárselo a una simulación de un brazo robot.
- Desarrollar una simulación mediante PeterCorke en python3.

## More About the Link Format for `.md` or `.wiki` files

  - (https://gist.github.com/subfuzion/0d3f19c4f780a7d75ba2#gistcomment-2684624)

 - For an image named `myimage.jpg` in an **`images` directory (or subdirectory below)**, the linking format follows by file type:

   ### .wiki:

       [[images/myimage.jpg]]
       [[/images/myimage.jpg]]

     - markdown `!()[]` syntax will not work

     `<img src="images/myimage.jpg">`
    
     - img tag works but only with relative path
     - does not support figure and figcaption tags

   ### test:

       [[images/myimage.jpg]]
       [[/images/myimage.jpg]]

       ![](../../blob/master/images/myimage.jpg)
    
     - the markdown `!()[]` syntax works but not relative paths

     `<img src="images/myimage.jpg">`
    
     - img tag works but only with relative path

     `<figure><img src="images/myimage.jpg"><figcaption>image caption</figcaption></figure>`
