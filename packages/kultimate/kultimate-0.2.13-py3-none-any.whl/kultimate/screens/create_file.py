from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, RadioButton, RadioSet


class CreateFile(ModalScreen[dict]):
    """Screen with a dialog to return yes or not"""

    BINDINGS = [
        ("escape", "exit", ""),
    ]

    def compose(self) -> ComposeResult:
        """Formar la pantalla"""
        yield Grid(
            Vertical(
                Input(
                    value="",
                    placeholder="Name for new file",
                    id="question-1",
                ),
                RadioSet(
                    RadioButton("Three Columns", value=True),
                    RadioButton("Five Columns"),
                ),
                id="the_vertical",
            ),
            id="the_new_file",
        )

    def action_exit(self) -> None:
        """Salir"""
        self.dismiss({"name_file": "", "columns": 0})

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        el_input = self.query_one(Input)
        name_file = el_input.value
        el_input.value = ""
        index = event.radio_set.pressed_index
        self.dismiss({"name_file": name_file, "columns": index})

    def on_input_submitted(self, event: Input.Submitted) -> None:
        the_text = event.input.value
        event.input.value = ""
        if event.input.id == "question-1":
            radio_set = self.query_one(RadioSet)
            index = radio_set.pressed_index
            self.dismiss({"name_file": the_text, "columns": index})
        else:
            self.dismiss({"name_file": "", "columns": 0})
