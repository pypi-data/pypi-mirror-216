from pathlib import Path

import yaml


class ProcessYaml:
    """Process Yaml"""

    home = Path.home()

    def set_path(self, name_file) -> None:
        """Get the content of file"""
        path = f"{self.home}/Dropbox/kanban2/{name_file}"
        if Path(path).is_file():
            self.yaml_file = path
            with open(self.yaml_file) as f:
                self.content_file = f.read()
            self.load_yaml()
        else:
            self.content_file = ""
            self.json_dir = {}

    def load_yaml(self):
        """Load yaml file"""
        self.json_dir = yaml.safe_load(self.content_file)

    def __show_home(self):
        """Mostrar el path del yaml_file"""
        print(self.yaml_file)

    def show_stages(self):
        """Show board's stages"""
        for stage in self.json_dir["stages"]:
            print(stage)

    def stages(self):
        """Get the board's stages (columns)"""
        return self.json_dir["stages"]


if __name__ == "__main__":
    process = ProcessYaml()
    process.set_path("todo.yml")
    process.show_stages()
