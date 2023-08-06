from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class DeleteTask(ModalScreen[bool]):
    """Screen with a dialog to return yes or not"""

    BINDINGS = [
        ("y", "say_yes", ""),
        ("c", "say_no", ""),
    ]

    def compose(self) -> ComposeResult:
        """Formar la pantalla"""
        yield Grid(
            Label(f"Delete task?", id="question"),
            Button("(Y)es", variant="error", id="yes"),
            Button("(C)ancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def action_say_yes(self) -> None:
        """Press y key"""
        self.dismiss(True)

    def action_say_no(self) -> None:
        """Press n key"""
        self.dismiss(False)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
