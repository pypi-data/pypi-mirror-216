from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Input


class EditTask(ModalScreen[str]):
    """Screen with a dialog for edit tasks"""

    BINDINGS = [
        ("escape", "exit", ""),
    ]

    def set_text(self, task_text: str) -> None:
        self.task_text = task_text

    def compose(self) -> ComposeResult:
        """Formar la pantalla"""
        yield Grid(
            Input(
                value=self.task_text,
                id="question",
            ),
            id="edit_task",
        )

    def action_exit(self) -> None:
        """Salir sin modificar la tarea"""
        self.dismiss(self.task_text)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        the_text = event.input.value
        event.input.value = ""
        if event.input.id == "question":
            self.dismiss(the_text)
        else:
            self.dismiss(self.task_text)
