import sys
from pathlib import Path

import pyperclip
from textual.app import App, ComposeResult
from textual.css.query import QueryError
from textual.reactive import var
from textual.widgets import Footer, Header

from .screens import AddTask, CreateFile, DeleteTask, EditTask, SelectAFile
from .utils import MarkTask, ParserMarkdown, StagesToMarkdown, create_new_markdown_file
from .widgets import Directory, Stage, StagesContainer, Task

# DONE: Hay errores al navegar entre las columnas.


class KanbanUltimate(App):
    """The main app class"""

    TITLE = "KUltimate"
    SUB_TITLE = "Using Kanban with Markdown"
    CSS_PATH = "app.css"
    SCREENS = {
        "delete_task": DeleteTask,
        "add_task": AddTask,
        "select_file": SelectAFile,
        "edit_task": EditTask,
        "create_file": CreateFile,
    }

    BINDINGS = [
        ("s", "select_file", "Select File"),
        # opción temporal, el archivo se debe guardar
        # cada que se modifique el contenido
        ("a, i", "add_task", "Add Task"),  # DONE: Guardar archivo
        ("e", "edit_task", "Edit Task"),  # DONE: Guardar archivo
        ("ctrl+l", "mark_as_done", "Mark as Done"),  # DONE: Guardar archivo
        ("ctrl+d", "delete_task", "Delete Task"),  # DONE: Guardar archivo
        ("ctrl+n", "new_file", "Create New File"),  # DONE: Guardar archivo
        ("q", "quit", "Quit"),
        # inician las teclas sin leyendas
        ("¡", "mark_as_important"),
        ("l, right", "go_to_right"),
        ("h, left", "go_to_left"),
        ("j, down", "go_to_down"),
        ("k, up", "go_to_up"),
        ("J, shift+down", "move_down"),  # DONE: Guardar archivo
        ("K, shift+up", "move_up"),  # DONE: Guardar archivo
        ("H, shift+left", "move_left"),  # DONE: Guardar archivo
        ("L, shift+right", "move_right"),  # DONE: Guardar archivo
        ("ctrl+c", "copy_task_to_clipboard"),
    ]

    home_user = Path.home()
    # home_directory = "Dropbox/kanban2"
    is_directory_visible = False
    total_stages = 0
    current_stage = 0
    # Classes para la columna y la tarea activa
    class_for_active_stage = "_actual"
    class_for_active_task = "_active"
    class_for_important_task = "_is_important"
    # Archivo md en el que se está trabajando
    actual_file = var("")
    # Variables para las tareas
    # poner a cero cuando se presione l o h
    current_task = 0
    total_tasks = 0
    # variable para guardar los archivos
    stages_to_markdown = StagesToMarkdown()

    def __init__(self, path: str) -> None:
        """init kultimate"""
        self.kanban_directory = path
        self.SUB_TITLE = path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with StagesContainer(id="stages_container"):
            yield Directory(self.kanban_directory, id="directory")
        yield Footer()

    def __new_active_task(self, old_task) -> None:
        """Elimina la clase self.class_for_active_task de la
        old_task y la agrega para current_task.
        Funciona para la misma columna."""
        try:
            self.list_tasks[old_task].remove_class(self.class_for_active_task)
            self.list_tasks[self.current_task].add_class(
                self.class_for_active_task,
            )
            self.__focus_task()
        except IndexError:
            pass

    def __unselect_task(self) -> None:
        """Quita la clase self.class_for_active_task de self.current_task"""
        try:
            self.list_tasks[self.current_task].remove_class(
                self.class_for_active_task,
            )
        except IndexError:
            pass

    def __select_task(self) -> None:
        """Agrega la clase self.class_for_active_task de self.current_task"""
        try:
            self.list_tasks[self.current_task].add_class(
                self.class_for_active_task,
            )
            self.__focus_task()
        except IndexError:
            pass

    def __remove_class_active_for_stage(self, stage: int) -> None:
        """remove self.class_for_active_stage"""
        try:
            self.list_stages[stage].remove_class(self.class_for_active_stage)
        except IndexError:
            pass

    async def __remove_task(self, task: int) -> None:
        """Remove task from self.list_tasks"""
        try:
            self.list_tasks[task].remove()
        except IndexError:
            pass

    def __update_list_tasks(self, stage: int) -> None:
        """Actualiza la lista de tareas"""
        try:
            self.list_tasks = self.list_stages[stage].query(Task)
            self.total_tasks = len(self.list_tasks) - 1
            self.current_task = 0
        except QueryError:
            self.total_tasks = 0
            self.current_task = 0
            pass

    def __add_class_for_active_task(self, current_task: int) -> None:
        """Add class self.class_for_active_task"""
        try:
            self.list_tasks[current_task].add_class(self.class_for_active_task)
            self.list_tasks[current_task].scroll_visible(force=True)
        except IndexError:
            pass

    # def __remove_class_for_active_task(self, current_task: int) -> None:
    #     """Add class self.class_for_active_task"""
    #     try:
    #         self.list_tasks[current_task].remove_class(
    #             self.class_for_active_task,
    #         )
    #     except IndexError:
    #         pass

    def __add_class_for_active_stage(self, stage: int) -> None:
        """Add class self.class_for_active_stage"""
        try:
            self.list_stages[stage].add_class(self.class_for_active_stage)
        except IndexError:
            pass

    def __activate_stage(
        self,
        old_stage: int,
        scroll_to_task: bool = True,
    ) -> None:
        """Elimina la clase self.class_for_active_stage para la
        columna old_stage y la agrega para current_stage.
        Modifica self.current_stage"""
        try:
            self.list_stages[old_stage].remove_class(
                self.class_for_active_stage,
            )
            self.list_stages[self.current_stage].add_class(
                self.class_for_active_stage,
            )
            self.list_stages[self.current_stage].scroll_visible()
            self.current_task = 0
            if self.list_stages:
                self.list_tasks = self.list_stages[self.current_stage].query(
                    Task,
                )
                # DONE: Obtener el total de tareas en la columna
                self.total_tasks = len(self.list_tasks) - 1
            else:
                self.total_tasks = 0

            if scroll_to_task:
                self.__select_task()
        except IndexError:
            pass

    # observar la variable self.actual_file
    def watch_actual_file(self) -> None:
        """Watch self.actual_file"""
        # por alguna razón hay que poner sub_title en minúsculas, no en
        # mayúsculas, o no funciona
        self.sub_title = self.actual_file
        self.stages_to_markdown.set_file(self.actual_file)

    def get_total_stages(self) -> None:
        try:
            self.list_stages = self.query(Stage)
            self.current_stage = 0
            self.__activate_stage(0)
            self.total_stages = len(self.list_stages) - 1
            self.__scroll_and_focus_stage()
            # Borrar después
        except QueryError:
            pass

    async def on_key(self) -> None:
        try:
            stages_container = self.query_one(StagesContainer)
            if not stages_container:
                await self.mount(StagesContainer())
                actual_stage = self.list_stages[self.current_stage]
                self.set_focus(actual_stage)
        except QueryError or IndexError:
            pass

    def set_title(self, title: str, sub_title: str = "") -> None:
        """Change TITLE and SUB_TITLE"""
        self.TITLE = title
        self.SUB_TITLE = sub_title

    def __actualize_total_tasks(self) -> None:
        """Actualiza el total de las tareas"""
        try:
            # current_stage solo es para acortar la siguiente línea
            current_stage = self.current_stage
            self.list_tasks = self.list_stages[current_stage].query(Task)
            self.total_tasks = len(self.list_tasks) - 1
        except IndexError:
            pass

    def action_copy_task_to_clipboard(self) -> None:
        """Copia la tarea al portapapeles"""
        try:
            text_to_copy = str(self.list_tasks[self.current_task].renderable)
            pyperclip.copy(text_to_copy)
        except IndexError:
            pass

    def action_add_task(self) -> None:
        """Add new task"""

        def get_value_from_input(text_for_new_task: str) -> None:
            """Obtiene el valor de la tarea"""
            if text_for_new_task != "":
                # realizar las operaciones necesarias para agregar la tarea
                # ¿Dónde montar la nueva tarea? ¿Al principio? ¿Al final?
                # ¿En la primer columna?
                # Montar la tarea en la columna actual
                new_task = Task(text_for_new_task)
                self.list_stages[self.current_stage].mount(new_task)
                old_task = self.current_task
                self.__actualize_total_tasks()
                self.current_task = self.total_tasks
                self.__new_active_task(old_task)

                # guardar al archivo
                self.__save_to_file()

        if self.actual_file:
            self.push_screen("add_task", get_value_from_input)
        else:
            self.push_screen("select_file")

    def action_edit_task(self) -> None:
        """Edit self.current_task"""

        def new_value_for_task(new_text_for_task: str) -> None:
            """Obtiene el valor de la tarea"""
            self.list_tasks[self.current_task].update(new_text_for_task)
            # guardar al archivo
            self.__save_to_file()

        if self.actual_file:
            task_text = str(self.list_tasks[self.current_task].renderable)
            screen_edit = EditTask()
            screen_edit.set_text(task_text)
            self.push_screen(screen_edit, new_value_for_task)

    def action_delete_task(self) -> None:
        """Delete task from stage"""

        async def check_delete_task(delete_task: bool) -> None:
            """Called when DeleteTask is dismissed"""
            if delete_task:
                if len(self.list_tasks) > 0:
                    await self.list_tasks[self.current_task].remove()
                    # actualizar self.total_tasks
                    self.__actualize_total_tasks()

                    if self.current_task == self.total_tasks + 1:
                        self.current_task = self.total_tasks

                    # resaltar la nueva tarea y hacer scroll
                    self.__select_task()

                    # guardar al archivo
                    self.__save_to_file()

        self.push_screen("delete_task", check_delete_task)

    def action_new_file(self) -> None:
        """Create a new file on directory"""

        async def create_new_file(dictionary: dict) -> None:
            """Function to create a new file"""
            create_new_markdown_file(self.kanban_directory, dictionary)
            try:
                directory = self.query_one(Directory)
                directory.reload()
            except QueryError:
                sys.exit(1)

        self.push_screen("create_file", create_new_file)

    async def action_mark_as_done(self) -> None:
        """Send task to last stage"""
        if self.current_stage == self.total_stages or self.total_tasks + 1 == 0:
            # Si estamos en la última columna, no hay nada que hacer
            # Si el total de tareas es cero, no hay nada que hacer
            return

        # copiar el texto de la tarea
        text_task_done = self.list_tasks[self.current_task].renderable
        # eliminar la tarea de la columna actual
        await self.list_tasks[self.current_task].remove()
        # actualizar self.total_tasks y self.current_task

        self.__actualize_total_tasks()

        if self.current_task == self.total_tasks + 1:
            self.current_task = self.total_tasks

        # resaltar la nueva tarea y hacer scroll
        self.__select_task()
        # crear una nueva tarea
        task_done = Task(text_task_done)
        # agregar a la última columna
        self.list_stages[self.total_stages].mount(task_done)

        # guardar al archivo
        self.__save_to_file()

    def action_select_file(self) -> None:
        """Toggle class for Directory"""
        directory = self.query_one(Directory)
        directory.toggle_class("_visible")
        self.is_directory_visible = not self.is_directory_visible

        if self.is_directory_visible:
            self.set_focus(directory)
        else:
            stages_container = self.query_one(StagesContainer)
            self.set_focus(stages_container)

    def __scroll_and_focus_stage(self) -> None:
        """Move scroll and focus a stage"""
        # Esta es la función que se llama cuando se cambia de columna
        self.__activate_stage(self.current_stage)
        # Hasta aquí las operaciones para la columna

        # Ahora las operaciones para las tareas

        self.current_task = 0
        try:
            self.list_tasks = self.list_stages[self.current_stage].query(Task)
            # DONE: Obtener el total de tareas en la columna
            self.total_tasks = len(self.list_tasks) - 1
        except IndexError:
            self.total_tasks = 0

        if self.list_tasks:
            self.__select_task()
            self.__focus_task()

    def __focus_task(self) -> None:
        """Move scroll and focus a task"""

        if self.list_tasks:
            self.list_tasks[self.current_task].focus(True)
            self.list_tasks[self.current_task].scroll_visible()

    def write_right(self) -> None:
        """Auxiliary function"""
        with open("/home/felipe/Dropbox/kanban2/subtitle.txt", "a") as ff:
            ff.write(f"subtitle modificado {self.SUB_TITLE}\n")

    def action_go_to_right(self) -> None:
        """Go right stage"""

        self.__unselect_task()

        self.current_task = 0
        self.total_tasks = 0

        old_stage = self.current_stage
        if len(self.list_stages):
            if self.current_stage < self.total_stages:
                self.current_stage += 1
            else:
                self.current_stage = 0

        self.__activate_stage(old_stage)

    def action_go_to_left(self) -> None:
        """Go left stage"""

        self.__unselect_task()

        if len(self.list_stages):
            old_stage = self.current_stage

            if self.current_stage > 0:
                self.current_stage -= 1
            else:
                self.current_stage = self.total_stages

            self.__activate_stage(old_stage)

    def action_mark_as_important(self) -> None:
        """Marcar la tarea como importante"""
        # Comprobar si existen tareas
        try:
            if not self.list_tasks:
                return
        except AttributeError:
            return

        # obtener el texto de la tarea
        text_for_task = str(self.list_tasks[self.current_task].renderable)
        # pasarla por MarkTask
        the_task = MarkTask(text_for_task)
        # actualizar la tarea
        the_task.toggle()
        self.list_tasks[self.current_task].update(the_task.line)
        if the_task.is_important:
            # si es importante, agregar la clase self.is_important
            self.list_tasks[self.current_task].add_class(self.class_for_important_task)
        else:
            # si no lo es, quitar la clase self.is_important
            self.list_tasks[self.current_task].remove_class(
                self.class_for_important_task
            )
        # guardar a disco
        self.__save_to_file()

    # DONE: Moverse entre tareas con j y k
    def action_go_to_down(self) -> None:
        """Ir a la tarea de abajo"""
        # ¿en qué columna estoy?
        # obtener la tarea activa: self.current_task es la tarea actual
        # quitar la clase de tarea activa
        if self.list_tasks:
            old_task = self.current_task
            # ir abajo
            if self.current_task < self.total_tasks:
                self.current_task += 1
            else:
                self.current_task = 0
            # poner clase de tarea activa
            self.__new_active_task(old_task)

    def action_go_to_up(self) -> None:
        """Ir a la tarea de arriba"""
        if self.list_tasks:
            old_task = self.current_task
            # ir arriba
            if self.current_task > 0:
                self.current_task -= 1
            else:
                self.current_task = self.total_tasks
            # poner clase de tarea activa
            self.__new_active_task(old_task)

    def interchange_task(self, index) -> None:
        """Intercambia las tareas"""

        if (
            index == 0
            and self.current_task == self.total_tasks
            and self.total_tasks != 1
        ):
            return

        if (
            index == self.total_tasks
            and self.current_task == 0
            and self.total_tasks != 1
        ):
            return

        if index != self.current_task:
            try:
                # quitar la clase a la tarea actual
                self.__unselect_task()

                # remover la clase self.class_for_important_task de ambas tareas
                self.list_tasks[self.current_task].remove_class(
                    self.class_for_important_task
                )
                self.list_tasks[index].remove_class(self.class_for_important_task)

                # hacer el intercambio de contenido
                actual_text = str(self.list_tasks[self.current_task].renderable)
                next_text = str(self.list_tasks[index].renderable)

                self.list_tasks[self.current_task].update(next_text)
                self.list_tasks[index].update(actual_text)
                # doing

                # establecer la nueva self.current_task
                self.current_task, index = index, self.current_task
                # si alguna tarea es importante añadir la clase
                # next_text ahora tiene el texto de self.current_task
                text_ = MarkTask(next_text)
                if text_.is_important:
                    self.list_tasks[index].add_class(self.class_for_important_task)
                # actual_text ahora tiene el texto de index
                text2_ = MarkTask(actual_text)
                if text2_.is_important:
                    self.list_tasks[self.current_task].add_class(
                        self.class_for_important_task,
                    )

                # agregar la clase activa
                self.__select_task()
            except IndexError:
                pass

    def action_move_down(self) -> None:
        """Mover la tarea hacia abajo. Se presionó la tecla J"""

        index = self.current_task
        if index < self.total_tasks:
            index += 1
        else:
            index = 0

        self.interchange_task(index)

        # guardar al archivo
        self.__save_to_file()

    def action_move_up(self) -> None:
        """Mover la tarea hacia abajo. Se presionó la tecla K"""
        # DONE: Mover el elemento hacia arriba
        index = self.current_task
        if index > 0:
            index -= 1
        else:
            index = self.total_tasks

        self.interchange_task(index)

        # guardar al archivo
        self.__save_to_file()

    async def move_task(self, new_stage) -> None:
        """mover tarea entre columnas, esta recibe la nueva columna
        a la cual se va a mover, por tanto, self.current_stage
        es la columna actual"""
        if new_stage != self.current_stage:
            # ambas columnas son distintas

            # guardar el texto de la tarea a mover
            text_to_move = self.list_tasks[self.current_task].renderable
            # remover la tarea de la columna actual
            await self.__remove_task(self.current_task)
            # DONE: Separar select y unselect stage
            # quitar la clase self.class_for_active_stage de la columna actual
            old_stage = self.current_stage
            self.__remove_class_active_for_stage(old_stage)
            # actualizar self.list_tasks - creo que esto no es necesario
            # Moverse a la nueva columna
            self.current_stage = new_stage
            self.__update_list_tasks(new_stage)
            # agregar self.class_for_active_stage a la nueva columna
            self.__add_class_for_active_stage(new_stage)
            # agregar la tarea a la nueva columna
            moved_task = Task(text_to_move)
            await self.list_stages[new_stage].mount(moved_task)
            self.__update_list_tasks(new_stage)
            self.current_task = self.total_tasks
            # agregar self.class_for_active_task a la tarea agregada
            self.__add_class_for_active_task(self.current_task)
            task_text = str(self.list_tasks[self.current_task].renderable)
            task_ = MarkTask(task_text)
            if task_.is_important:
                self.list_tasks[self.current_task].add_class(
                    self.class_for_important_task
                )
            # actualizar self.list_tasks

    async def action_move_left(self) -> None:
        """Mover la tarea a la columna de la izquierda. Se presionó H"""
        new_stage = self.current_stage
        if new_stage > 0:
            new_stage -= 1
        else:
            new_stage = self.total_stages

        await self.move_task(new_stage)

        # guardar al archivo
        self.__save_to_file()

    async def action_move_right(self) -> None:
        """Mover la tarea a la columna de la derecha. Se presionó L"""
        new_stage = self.current_stage
        if new_stage < self.total_stages:
            new_stage += 1
        else:
            new_stage = 0

        await self.move_task(new_stage)

        # guardar al archivo
        self.__save_to_file()

    def __save_to_file(self) -> None:
        """Guardar el archivo. Función temporal,
        pues no será llamada directamente, sino cada vez
        que se modifique el contenido"""
        if self.actual_file:
            # actualizar stages
            try:
                self.list_stages = self.query(Stage)
                self.stages_to_markdown.set_file(self.actual_file)
                self.stages_to_markdown.structure_to_markdown(self.list_stages)
            except QueryError:
                pass

    async def unmount_stages(self) -> None:
        """Desmonta las columnas"""
        # DONE: Desmontar las columnas actuales - usar remove
        try:
            stages = self.query(Stage)
            for stage in stages:
                await stage.remove()
        except IndexError:
            pass

    async def mount_stages(self) -> None:
        """Monta las columnas"""
        # DONE: Montar las nuevas columnas. Usar mount
        try:
            stages_container = self.query_one("#stages_container")
            board = self.parser_content.get_board()
            # DONE: Montar tareas en las columnas
            index = 0
            for stage in board.keys():
                new_stage = Stage()
                new_stage.set_title(stage)
                # DONE:Errores al desplegar los movimientos entre J y K
                # DONE: Mover tareas con H y L
                first_task = True
                for task in board[stage]:
                    new_task = Task(task)
                    # determinar si es una tarea importante
                    important_task = MarkTask(task)
                    if important_task.is_important:
                        new_task.add_class(self.class_for_important_task)

                    await new_stage.mount(new_task)
                    # DONE: Que la primer tarea obtenga el foco
                    if index == 0 and first_task:
                        new_task.focus()
                        first_task = False
                        new_task.add_class(self.class_for_active_task)

                await stages_container.mount(new_stage)
                index += 1

            self.get_total_stages()

            self.__scroll_and_focus_stage()
            # self.current_task = self.total_tasks
            self.__focus_task()

        except IndexError:
            pass

    # DONE: Seleccionar un archivo para mostrar.
    # File selected
    async def on_directory_tree_file_selected(
        self,
        event: Directory.FileSelected,
    ) -> None:
        event.stop()
        self.actual_file = str(event.path)
        # Ocultar Directory
        self.parser_content = ParserMarkdown(self.actual_file)
        self.action_select_file()
        await self.unmount_stages()
        await self.mount_stages()
        self.refresh()


def main(path: str) -> None:
    KanbanUltimate(path).run()
