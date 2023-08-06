# Kultimate

![kultimate](render1686782901985.gif)

Aplicación CLI Python para manejar archivos markdown como tableros Kanban.
Programado con [textual](https://textual.textualize.io/).

## Requerimientos

`python = "^3.10"`

## Instalación

```sh
pip install kultimate
```

## Configuración

Trabajo en progreso

## Uso

|                     | Teclas para operar la aplicación              |
| ------------------- | --------------------------------------------- |
| ¡                   | Marcar/desmarcar tarea como importante        |
| j, flecha abajo     | ir a la tarea de abajo                        |
| k, flecha arriba    | ir a la tarea de arriba                       |
| l, flecha izquierda | ir a la columna de la derecha                 |
| h, flecha derecha   | ir a la columna de la izquierda               |
| J                   | Llevar la tarea hacia arriba                  |
| K                   | Llevar la tarea hacia abajo                   |
| L                   | Cambiar la tarea a la columna de la derecha   |
| H                   | Cambiar la tarea a la columna de la izquierda |
| s                   | Seleccionar un archivo para abrirlo           |
| a, i                | Agregar tarea al final de la columna actual   |
| ctrl+l              | Mueve la tarea a la última columna            |
| ctrl+d              | Borra la tarea seleccionada                   |
| ctrl+c (ver nota)   | Copiar la tarea al portapapeles               |
| q                   | Salir de la aplicación                        |

`Nota para la copia de tareas al portapaleles`:

> En Linux se debe instalar xclip, xsel o wl-clipboard (para las sesiones en
> wayland). Por ejemplo, en Debian:
>
> ```sh
> sudo apt-get install xclip
> sudo apt-get install xsel
> sudo apt-get install wl-clipboard
> ```

## ToDo

- [ ] TODO: Agregar recordatorios
- [ ] TODO: Corregir uso de directorios
- [ ] DONE: Al cambiar la última tarea con J, se intercambia con la primera.
      Quiero que solo se ponga encima. Hace lo mismo cuando se usa K en la
      primer tarea, se intercambia con la última.
- [ ] DONE: Copiar tareas al portapapeles
- [x] DONE: Corregir el uso de ctrl-l
- [x] DONE: Marcar tareas importantes
- [x] DONE: Al cargar las tareas, agregar clase de importante si la marca está
      presente
- [x] DONE: Crear nuevo archivo. Usar el esqueleto creado en el archivo de configuración
- [x] DONE: Rehacer la configuración de la aplicación.
- [x] DONE: Hacer esqueleto para crear los nuevos archivos.
- [x] DONE: Si no existe directorio crearlo.
- [x] DONE: Reducir el tamaño de la caja para capturar las tareas.
- [x] DONE: Editar tareas
- [x] DONE: Al mover las tareas entre columnas visualmente se ve bien, pero al
      grabar a disco se queda en todas las columnas por donde pasa.
- [x] DONE: Grabar a disco.
- [x] DONE: Agregar tareas.
- [x] DONE: preguntar antes de borrar la tarea.
- [x] DONE: Borrar tareas.
- [x] DONE: Enviar tareas a la última columna.
- Operaciones en archivo.
  - [x] DONE: Convertir html a markdown al grabar.
  - [x] DONE: Grabar el archivo a disco.

## Quizás

- [ ] TODO: Agregar columnas.
- [ ] TODO: Mover columnas.
- [ ] TODO: Duplicar tareas.
- [ ] TODO: Agregar sub tareas.
- [ ] TODO: Crear un color nuevo para la última columna.
- [ ] TODO: Seleccionar tareas con click del ratón.
- [x] DONE: Cambiar Task al widget Input.
- [x] DONE: Filtrar los archivos por extensión..
- [x] DONE: de Markdown a html.
- [x] DONE: del html extraer la info con beautifulsoup.
- [x] DONE: Que aparezca el nombre del archivo en la cabecera de la aplicación.
- [x] DONE: Crear las columnas al cambiar de archivo usar mount y remove.
- [x] DONE: ¿Por qué se "dispara" el scroll horizontal, si no estoy agregando.
      nuevos elementos? R: Cada que se cargaba un nuevo archivo se montaba un.
      StageContainer por cada columna.
- [x] DONE: Al cambiar a una columna sin tareas se truena el programa.
- [x] DONE: Primero debo corregir lo del foco al cargar el archivo.
- [x] DONE: No funciona al presionar la primera H, hasta la segunda. En realidad no
      funciona la primera tecla.
- [x] DONE: En general no detecta la primera letra que se presiona al seleccionar
      un archivo.
- [x] DONE: al presionar primero la tecla k (go_to_up) no se mueve correctamente a
      la última tarea.
- [x] DONE: al mover una tarea hacia la primer columna, si se tiene que hacer
      scroll, una vez se hace correctamente, y otra no.
