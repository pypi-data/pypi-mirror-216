from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Input


class AddTask(ModalScreen[str]):
    """Screen with a dialog to return yes or not"""

    BINDINGS = [
        ("escape", "exit", ""),
    ]

    def compose(self) -> ComposeResult:
        """Formar la pantalla"""
        yield Grid(
            Input(
                value="",
                placeholder="Write the new task",
                id="question",
            ),
            id="add_task",
        )

    def action_exit(self) -> None:
        """Salir"""
        self.dismiss("")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        the_text = event.input.value
        event.input.value = ""
        if event.input.id == "question":
            self.dismiss(the_text)
        else:
            self.dismiss("")
