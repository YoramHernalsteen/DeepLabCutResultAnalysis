import utils.config_utils as config_utils
import os

from typing import List

def files_not_converted(type: str) -> List[str]:
    """Compares files in input and output folders and returns those in the input but not the output."""
    missing_files = []
    if type is None or not isinstance(type, str):
        type = ''
    
    input_folder = config_utils.input_path()
    output_folder = config_utils.output_path()
    
    for filename in os.listdir(input_folder):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, type + convert_filename_to_tiff(filename))
        if os.path.isfile(input_file) and is_csv(input_file) and not os.path.isfile(output_file):
            missing_files.append(input_file)
    
    return missing_files

def is_csv(file_path):
    ext = os.path.splitext(file_path)[1]
    image_extensions = [".csv"]  # Add more as needed
    return ext.lower() in image_extensions

def convert_filename_to_png(filename):
    root, _ = os.path.splitext(filename)
    return root + '.png'

def convert_filename_to_csv(filename):
    root, _ = os.path.splitext(filename)
    return root + '.csv'

def convert_filename_to_tiff(filename, prefix = None, postfix = None):
    root, _ = os.path.splitext(filename)
    if prefix is not None and isinstance(prefix, str):
        root = prefix + '_' + root
    if postfix is not None and isinstance(postfix, str):
        root = root + '_' + postfix
    return root + '.tiff'

def input_files() -> List[str]:
    """returns all files in the input folder."""
    files = []

    input_folder = config_utils.input_path()
    
    for filename in os.listdir(input_folder):
        if is_csv(filename):
            files.append(os.path.join(input_folder, filename))
    
    return files

def base_filename(filepath):
    return os.path.basename(filepath)

def verify_output_folder() -> None:
    """Verifies output folder is present and creates it if necessary."""
    if not os.path.exists(config_utils.output_path()):
        os.makedirs(config_utils.output_path(), exist_ok=True)

def generate_output_file_location(file: str) -> str:
    """Generates the correct file location in the output folder for a given filename."""
    return os.path.join(config_utils.output_path(), convert_filename_to_png(file))

def generate_output_file_location_csv(file: str) -> str:
    """Generates the correct file location in the output folder for a given filename."""
    return os.path.join(config_utils.output_path(), convert_filename_to_csv(file))