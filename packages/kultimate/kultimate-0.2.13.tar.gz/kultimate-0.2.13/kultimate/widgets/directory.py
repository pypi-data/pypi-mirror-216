from pathlib import Path
from typing import Iterable

from textual.binding import Binding
from textual.widgets import DirectoryTree

# DONE: Aparecer y desaparecer el elemento Directory
# DONE: Perder el foco cuando se oculte el widget


class Directory(DirectoryTree):
    """Wrap DirectoryTree"""

    BINDINGS = [
        Binding("j", "cursor_down", "", False),
        Binding("k", "cursor_up", "", False),
        Binding("space, enter, l", "select_cursor", "", False),
    ]

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if path.name.endswith(".md")]
