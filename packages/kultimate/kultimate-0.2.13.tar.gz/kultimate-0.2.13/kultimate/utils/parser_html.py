import markdown
from bs4 import BeautifulSoup
from rich import print


class ParserMarkdown:
    """Procesar el html generado a partir de markdown"""

    def __init__(self, file_path):
        """Obtiene el contenido del archivo"""

        self.file_path = file_path
        with open(self.file_path) as ff:
            content = ff.read()

        html_content = markdown.markdown(content)

        self.soup = BeautifulSoup(html_content, features="html.parser")

    def get_stages(self):
        """Obtiene todos los h2 del documento"""
        try:
            h2s = self.soup.select("h2")
        except IndexError:
            h2s = []
        return h2s

    def pretty(self):
        """Imprime el html en un bonito formato"""
        return self.soup.prettify()

    def get_board(self):
        """Obtiene todas las tareas de cada h2"""
        # doing
        # aquí es donde tengo el error, cuando no hay tareas en la
        # primer columna empiezan las fallas
        # obtener todos los h2, y de ahí todos los li
        # DONE: Cargar las tareas desde el archivo
        tasks = {}
        # ¿una lista de listas? Mejor un diccionario
        # {1:["strings", "string"], 2:["string", "string"]}
        # primero obtener todos los h2
        h2s = self.soup.find_all("h2")
        # ahora obtener los li de cada h2

        for h2 in h2s:
            list_tasks = []
            next_sibling = h2.find_next_sibling()
            if next_sibling == None or next_sibling.name == "h2":
                tasks[h2.text] = list_tasks
                continue

            if next_sibling.name == "ul":
                for li in next_sibling.findChildren("li"):
                    list_tasks.append(li.text.strip())

                tasks[h2.text] = list_tasks
            else:
                tasks[h2.text] = list_tasks
                continue

        return tasks
