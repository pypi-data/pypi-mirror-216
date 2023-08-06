import html2text
import markdown
from rich import print
from textual.css.query import QueryError

from ..widgets import Task


class StagesToMarkdown:
    """Convertir html a markdow"""

    markdown_text = ""
    html_text = ""
    name_file = ""

    # Me pregunto si necesito convertir de html a markdown,
    # es probable que solo necesite recorrer la lista y escribir el archivo.

    def set_file(self, name_file: str) -> None:
        """init name_file"""
        self.name_file = name_file

    def to_markdown(self, html: str) -> str:
        """Convertir html a markdown, para poder escribirlo"""
        # DONE: Convertir html a markdown al grabar
        self.markdown_text = html2text.html2text(html)
        print(self.markdown_text)
        return self.markdown_text

    def to_html(self, text_markdown: str) -> None:
        """Convertir markdown a html"""
        self.html_text = markdown.markdown(text_markdown)
        print(self.html_text)

    def write_to_file(self) -> None:
        """Escribir markdown en el archivo dado"""
        # DONE: Grabar el archivo a disco
        with open(self.name_file, "w") as ff:
            ff.write(self.markdown_text)

    def structure_to_markdown(self, stage_list) -> None:
        """Convierte el contenido de stage_list a markdown"""
        # DONE: Convertir stage_list a markdown
        # DONE: modificar self.markdown_text
        self.markdown_text = ""

        # Obtener los nombres de las columnas
        for stage in stage_list:
            self.markdown_text += f"## {stage.title}\n\n"
            # Obtener las tareas para cada columna
            try:
                tasks = stage.query(Task)
                for task in tasks:
                    # texto = task.render()
                    self.markdown_text += f"- {task.renderable}\n"
            except QueryError:
                pass

            self.markdown_text += "\n"

        print(self.markdown_text)
        # DONE: Cuando acabe la función, descomentar la última línea
        self.write_to_file()
