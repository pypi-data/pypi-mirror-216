from configparser import ConfigParser
from pathlib import Path

from .app import main

user_home_directory = Path.home()
path_file_config = f"{user_home_directory}/.kultimate.ini"
config_object = ConfigParser()
