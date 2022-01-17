# TurtleBot Control App
Este es mi primera prueba tanto con Git como en Github.

El objetivo es aprender a utilizar un gestor de versiones y además un repositorio online para usarlo como copia de seguridad de mi proyecto para el TFG de ingeniería ROBÓTICA en la UA.

El objetivo del TFG es desarrollar una interfad de control hombre máquina de bajo coste para controlar brazos robot mediante visión por computador.

## De momento los objetivos son:

- Seguir testeando con MediaPipe.
- Ver si utilizar la Z que proporciona es factible para la profundidad. (Parece que si pero no es suficiente)
- Probar a obtener las coordenaadas articulares y pasárselo a una simulación de un brazo robot.
- Desarrollar una simulación mediante PeterCorke en python3.

<p align="center">
  <img src="clip.gif" alt="animated" href="https://google.com" />
</p>

[![Watch the video](https://youtu.be/<https://youtu.be/j-LswYOt--s>)

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
