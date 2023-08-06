import os
import sys
from configparser import ConfigParser
from os.path import exists

import typer
from rich import print

from .. import config_object, path_file_config, user_home_directory
from ..app import main

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# app = typer.Typer(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)

app = typer.Typer()


default_config = ConfigParser()

default_config["WORKING_DIRECTORY"] = {
    "path": f"{user_home_directory}/kultimate",
}


def check_directory(path: str) -> None:
    """Verifica si existe el directorio, si no, sale del programa"""
    working_directory_exists = exists(path)
    if working_directory_exists:
        main(path)
    else:
        print(f"Directory '{path}' not exists")
        print(f"Change 'path' on '{path_file_config}'")
        print(f"Creating directory '{path}'")
        try:
            os.makedirs(path)
            main(path)
        except PermissionError:
            print("PermissionError")
            print(f"'{path}' not created.")
            sys.exit(1)


@app.callback(invoke_without_command=True)
def init(path: str = ""):
    """Launch kanban ultimate for markdown"""
    file_config_exists = exists(path_file_config)

    if path:
        # Si el usuario introdujo un valor
        check_directory(path)
    elif file_config_exists:
        config_object.read(path_file_config)
        try:
            directory_info = config_object["WORKING_DIRECTORY"]
            working_path = directory_info["path"]
            check_directory(working_path)
        except IndexError:
            print("Error in config file")
            print(f"Please delete {path_file_config} and run kultimate again.")
            print("Or edit it and correct the path.")
    else:
        # DONE: Crear archivo con la configuración por default
        print("file config not exists")
        print(f"creating file {path_file_config}...")
        try:
            with open(path_file_config, "w") as conf:
                default_config.write(conf)
            print("run kultimate again")
        except PermissionError:
            print(f"Error Permission Writing config file '{path_file_config}'")


def run():
    app()
