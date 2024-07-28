import utils.constants as constants
import configparser
import os

from typing import List

def get_ini_value(section: str, option: str) -> str:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.get(section=section, option=option)

def get_dir_from_ini(section: str, option: str) -> str:
    return os.path.normpath(get_ini_value(section=section, option=option))

def ini_file_valid_dir_value(section: str, option: str) -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    if(not config.has_option(section=section, option=option)):
        return False
    
    if(config.get(section=section, option=option) == ''):
        return False
    
    return os.path.exists(os.path.normpath(config.get(section=section, option=option)))

def output_path() -> str:
    if not ini_file_has_output():
        return ''
    return get_dir_from_ini('IO', 'output')

def input_path() -> str:
    if not ini_file_has_input():
        return ''
    return get_dir_from_ini('IO', 'input')


def current_path() -> str:
    return os.getcwd()

def check_for_ini_file() -> bool:
    return os.path.isfile(os.path.join(current_path(),constants.ini_file))

def ini_file_has_output() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "output") and ini_file_valid_dir_value("IO", "output")

def ini_file_has_input() -> bool:
    config = configparser.ConfigParser()
    config.read(os.path.join(current_path(),constants.ini_file))
    return config.has_option("IO", "input") and ini_file_valid_dir_value("IO", "input")


def has_valid_ini_file():
    return check_for_ini_file() and ini_file_has_output() and ini_file_has_input()

def create_ini_file(input_folder: str, output_folder:str) -> None:
    config = configparser.ConfigParser()
    config['IO'] = {'input': input_folder, 'output': output_folder}
    with open(os.path.join(current_path(),constants.ini_file), 'w') as configfile:
        config.write(configfile)
        
