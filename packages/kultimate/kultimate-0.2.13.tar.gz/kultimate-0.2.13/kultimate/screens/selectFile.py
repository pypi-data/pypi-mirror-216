from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class SelectAFile(ModalScreen[bool]):
    """Screen with a dialog to return yes or not"""

    BINDINGS = [
        ("y", "say_ok", ""),
    ]

    def compose(self) -> ComposeResult:
        """Formar la pantalla"""
        yield Grid(
            Label("Select a file to add a task", id="question"),
            Button("Ok", variant="error", id="ok"),
            id="dialog",
        )

    def action_say_ok(self) -> None:
        """Press y key"""
        self.dismiss(True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(True)
        else:
            self.dismiss(False)
