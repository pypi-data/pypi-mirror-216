# import json
# from configparser import ConfigParser
from os.path import exists
from pathlib import Path

user_home_directory = Path.home()
path_file_config = f"{user_home_directory}/.kultimate.ini"
# config_object = ConfigParser()


def create_new_markdown_file(directory: str, dictio: dict) -> bool:
    """Create a new markdown directory on directory"""

    if not dictio["name_file"]:
        return False

    # file_config_exists = exists(path_file_config)

    stages_three = ["ToDo", "Doing", "Done"]
    stages_five = ["BackLog", "ToDo", "Doing", "Waiting", "Done"]

    # if file_config_exists:
    #     config_object.read(path_file_config)

    #     if "SKELETONS" in config_object:
    #         try:
    #             stages_three = json.loads(
    #                 config_object.get("SKELETONS", "three_stages"),
    #             )
    #             stages_five = json.loads(
    #                 config_object.get("SKELETONS", "five_stages"),
    #             )
    #         except IndexError:
    #             pass

    name_file = dictio["name_file"]
    if not name_file.endswith(".md"):
        name_file += ".md"

    new_file = f"{directory}/{name_file}"

    file_exists = exists(new_file)

    what_stage = dictio["columns"]

    if what_stage == 0:
        stages = stages_three
    else:
        stages = stages_five

    content = ""
    for stage in stages:
        content += f"## {stage}\n\n"

    if not file_exists:
        try:
            with open(new_file, "w") as ff:
                ff.write(content)
        except PermissionError:
            pass

    return True
