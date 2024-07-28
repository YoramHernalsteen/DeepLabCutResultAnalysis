import utils.config_utils as config
import utils.file_utils as file_utils
import utils.csv_utils as csv_utils
import analysis.path_analysis as path_analysis
import analysis.density_analysis as density_analysis 
import os

import utils.constants as constants

class Terminal():
    initialized: bool = False
    running: bool = False

    def initialize(self):
        while not config.has_valid_ini_file():
            print('First we need to create a valid configuration file!')
            print('Input folder:')
            input_folder = input()
            print('Output folder:')
            output_folder = input()
            config.create_ini_file(input_folder, output_folder)
            if not config.has_valid_ini_file():
                print('Oops! It seems the configuration is not valid!')
            else:
                print('Great! The configuration is valid. Let\'s start!')
                print('Start by typing a command.')
                print()
                print('Type in help for more information. Type in quit to quit.')
        
        self.initialized = True
        self.running = True

    def greet(self):
        print("\033[92m")
        print("         _._")
        print("      .-'   `")
        print("    __|__")
        print("   /     \\")
        print("   |()_()|")
        print("   \\{o o}/")
        print("    =\o/=")
        print("     ^ ^")
        print()
        print()
        print('Let\'s analyze animal behavior!')
        print()
        print('Start by typing a command.')
        print()
        print('Type in help for more information. Type in quit to quit.')
        print('')

    def evaluate_input(self, v: str):
        if v is None or not isinstance(v, str) or v.strip() == '':
            print('That command is not recognized, please try again.')
            return()
        
        v = v.strip()
        v_key = v.split(" ", 1)[0]
        if(len(v.split(" ", 1)) > 1):
            v = v.split(" ", 1)[1]
            v = v.strip()
        else:
            v = ''

        if v_key.lower() == 'quit':
            self.running = False
            return
        elif v_key.lower() == 'heatmap':
            bodypart_heatmap = v.split(" ", 1)[0]
            if bodypart_heatmap is None or bodypart_heatmap == '':
                print('Bodypart is not valid.')
                return
            for file in file_utils.input_files():
                data = csv_utils.read_body_part(bodypart_heatmap, file)
                file_name = file_utils.base_filename(file)
                output_file = file_utils.generate_output_file_location(file_utils.convert_filename_to_tiff(filename=file_name, prefix=f'{v_key}_{bodypart_heatmap}'))
                if os.path.exists(output_file):
                    os.remove(output_file)
                density_analysis.plot_density_map_continous(data, output_file)
            
            print('Generated all heatmaps. Please type in a command or quit.')
            return
        elif v_key.lower() == 'trace':
            bodypart_trace = v.split(" ", 1)[0]
            if bodypart_trace is None or bodypart_trace == '':
                print('Bodypart is not valid.')
                return
            for file in file_utils.input_files():
                data = csv_utils.read_body_part(bodypart_trace, file)
                file_name = file_utils.base_filename(file)
                output_file = file_utils.generate_output_file_location(file_utils.convert_filename_to_tiff(filename=file_name, prefix=f'{v_key}_{bodypart_trace}'))
                if os.path.exists(output_file):
                    os.remove(output_file)
                path_analysis.trace_path(data, output_file)
            
            print('Generated all trace plots. Please type in a command or quit.')
            return
        elif v_key.lower() == 'help':
            self.display_help()
            return
        else:
            print('That command is not recognized, please try again.')
            return

    def display_help(self):
        print('This terminal application is meant to make analyzing of deeplabcut csv files easier.')
        print('There are a couple of possible analysis functions including:')
        print(' * creating heatmaps: heatmap [bodypart]')
        print(' * creating a trace map of path followed: trace [bodypart]')
        print('')
        print(f'Data is read from input folder configured in the {constants.ini_file} file and stored in the output folder in the {constants.ini_file} file.')
        print('Data is then analyzed for each deeplabcut csv file.')

    def run(self):
        self.clear_screen()
        self.greet()
        self.initialize()
        while self.running:
            print('')
            print('---------------------------')
            v = input()
            self.evaluate_input(v)
        self.clear_screen()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')