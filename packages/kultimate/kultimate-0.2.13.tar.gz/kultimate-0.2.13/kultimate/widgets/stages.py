from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.reactive import reactive


class Stage(VerticalScroll):
    """Columnas del tablero"""

    title = ""

    def on_mount(self) -> None:
        self.border_title = self.title

    def set_title(self, title) -> None:
        """Establecer el título de la columna"""
        self.title = title
