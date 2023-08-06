class MarkTask:
    """Determina si una línea tiene la marca de importante o no"""

    important_mark = " @!!"

    def __init__(self, line: str) -> None:
        self.line = line
        self.is_important = False
        self.determine()

    def determine(self) -> None:
        """Determina si la línea tiene la marca de importante o no"""
        mark_present = self.line.find(self.important_mark)
        if mark_present == -1:
            # La marca no está presente
            self.is_important = False
        else:
            # La marca está presente
            self.is_important = True

    def toggle(self) -> None:
        """Determina si la linea tiene la marca de importante o no"""
        # important = self.determine()
        self.is_important = not self.is_important
        if self.is_important:
            ### ahora es verdadero, agregar la marca
            self.line += self.important_mark
        else:
            ### ahora es falso, quitar la marca
            self.line = self.line.replace(self.important_mark, "")
