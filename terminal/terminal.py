import os

import analysis.density_analysis as density_analysis
import analysis.path_analysis as path_analysis
import utils.config_utils as config
import utils.constants as constants
import utils.csv_utils as csv_utils
import utils.file_utils as file_utils
from terminal.argument_definition import ArgDefinition, CommandDefinition
from terminal.argument_type import ArgumentType
from terminal.parser import Parser


class Terminal:
    initialized: bool = False
    running: bool = False
    parser: Parser

    def initialize(self):
        self.check_for_valid_ini()
        self.initialize_parser()
        self.initialized = True
        self.running = True

    def check_for_valid_ini(self):
        while not config.has_valid_ini_file():
            print("First we need to create a valid configuration file!")
            print("Input folder:")
            input_folder = input()
            print("Output folder:")
            output_folder = input()
            config.create_ini_file(input_folder, output_folder)
            if not config.has_valid_ini_file():
                print("Oops! It seems the configuration is not valid!")
            else:
                print("Great! The configuration is valid. Let's start!")
                print("Start by typing a command.")
                print()
                print("Type in help for more information. Type in quit to quit.")

    def initialize_parser(self):
        self.parser = Parser()
        self.parser.add_command_definition(
            CommandDefinition("trace", "Trace the path taken by the mouse")
            .add_argument_definition(
                ArgDefinition(
                    "-b",
                    "bodypart",
                    "Choose bodypart of trace analysis",
                    ArgumentType.TYPE_STR,
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-d",
                    "distance",
                    "Show distance travelled in subtitle of plot",
                    ArgumentType.TYPE_DIMENSION,
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-s",
                    "speed",
                    "Show speed travelled in subtitle of plot",
                    ArgumentType.TYPE_DIMENSION,
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-sd",
                    "speed and distance",
                    "Show speed and distance travelled in subtitle of plot",
                    ArgumentType.TYPE_DIMENSION,
                )
            )
        )
        self.parser.add_command_definition(
            CommandDefinition(
                "heatmap", "Create a heatmap of places most visited"
            ).add_argument_definition(
                ArgDefinition(
                    "-b",
                    "bodypart",
                    "Choose bodypart of trace analysis",
                    ArgumentType.TYPE_STR,
                )
            )
        )
        self.parser.add_command_definition(
            CommandDefinition("quit", "Quit the application")
        )

        self.parser.add_command_definition(
            CommandDefinition(
                "trace_csv",
                "Create a csv with speed, distance, ... of all files of a bodypart",
            )
            .add_argument_definition(
                ArgDefinition(
                    "-b",
                    "bodypart",
                    "Choose bodypart of trace analysis",
                    ArgumentType.TYPE_STR,
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-s", "size", "size of the box", ArgumentType.TYPE_DIMENSION
                )
            )
        )
        self.parser.add_command_definition(
            CommandDefinition(
                "dist_interval_csv",
                "Create a csv per file with distance and speed per interval",
            )
            .add_argument_definition(
                ArgDefinition(
                    "-b",
                    "bodypart",
                    "Choose bodypart of trace analysis",
                    ArgumentType.TYPE_STR,
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-t", "time", "Time interval in seconds", ArgumentType.TYPE_INT
                )
            )
            .add_argument_definition(
                ArgDefinition(
                    "-s", "size", "size of the box", ArgumentType.TYPE_DIMENSION
                )
            )
        )

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
        print("Let's analyze animal behavior!")
        print()
        print("Start by typing a command.")
        print()
        print("Type in help for more information. Type in quit to quit.")
        print("")

    def evaluate_input(self, v: str):
        command = self.parser.parse(v)
        if command is None:
            print("That command is unknown, please try again")
            return

        if command.command == "quit":
            self.running = False
            return
        elif command.command == "heatmap":
            bodypart = command.get_argument("bodypart").value
            if bodypart is None:
                print("Bodypart is not valid.")

            for file in file_utils.input_files():
                data = csv_utils.read_body_part(bodypart, file)
                file_name = file_utils.base_filename(file)
                output_file = file_utils.generate_output_file_location(
                    file_utils.convert_filename_to_tiff(
                        filename=file_name, prefix=f"{command.command}_{bodypart}"
                    )
                )
                if os.path.exists(output_file):
                    os.remove(output_file)
                density_analysis.plot_density_map_continous(data, output_file)

            print("Generated all heatmaps. Please type in a command or quit.")
            return
        elif command.command == "trace":
            bodypart = command.get_argument("bodypart").value
            if bodypart is None:
                print("Bodypart is not valid.")
            calculate_distance = False
            calculate_speed = False
            real_size = ""
            if command.has_argument("speed and distance"):
                calculate_speed = True
                calculate_distance = True
                real_size = command.get_argument("speed and distance").value
            if command.has_argument("speed"):
                calculate_speed = True
                real_size = command.get_argument("speed").value
            if command.has_argument("distance"):
                calculate_distance = True
                real_size = command.get_argument("distance").value

            for file in file_utils.input_files():
                data = csv_utils.read_body_part(bodypart, file)
                file_name = file_utils.base_filename(file)
                output_file = file_utils.generate_output_file_location(
                    file_utils.convert_filename_to_tiff(
                        filename=file_name, prefix=f"{command.command}_{bodypart}"
                    )
                )
                if os.path.exists(output_file):
                    os.remove(output_file)
                path_analysis.trace_path(
                    data, output_file, real_size, calculate_distance, calculate_speed
                )

            print("Generated all trace plots. Please type in a command or quit.")
            return
        elif command.command == "trace_csv":
            bodypart = command.get_argument("bodypart").value
            if bodypart is None:
                print("Bodypart is not valid.")

            real_size = command.get_argument("size")
            if real_size is None:
                print("Size is not valid.")
                return

            output_file = file_utils.generate_output_file_location_csv("analysis")
            if os.path.exists(output_file):
                os.remove(output_file)
            files = file_utils.input_files()
            path_analysis.create_path_analysis_table(
                output_file, files, real_size.value, bodypart
            )
            print("Generated csv analysis file. Please type in a command or quit.")
            return
        elif command.command == "dist_interval_csv":
            bodypart = command.get_argument("bodypart").value
            if bodypart is None:
                print("Bodypart is not valid.")

            real_size = command.get_argument("size")
            if real_size is None:
                print("Size is not valid.")
                return
            time_interval = 60
            if command.has_argument("time"):
                time_interval = int(command.get_argument("time").value)
            else:
                print("Using default time interval of 60 seconds.")

            for file in file_utils.input_files():
                data = csv_utils.read_body_part(bodypart, file)
                file_name = file_utils.base_filename(file)
                output_file = file_utils.generate_output_file_location_csv(
                    f"{command.command}_{bodypart}_{file_name}"
                )
                if os.path.exists(output_file):
                    os.remove(output_file)
                path_analysis.distance_interval_csv(
                    data, time_interval, real_size.value, output_file
                )

            print("Generated all distance csv`s. Please type in a command or quit.")
            return

    def display_help(self):
        print(
            "This terminal application is meant to make analyzing of deeplabcut"
            + " csv files easier."
        )
        print("There are a couple of possible analysis functions including:")
        print(" * creating heatmaps: heatmap [bodypart]")
        print(" * creating a trace map of path followed: trace [bodypart]")
        print("")
        print(
            f"Data is read from input folder configured in the {constants.ini_file}"
            + " file and stored in the output folder in the {constants.ini_file} file."
        )
        print("Data is then analyzed for each deeplabcut csv file.")

    def run(self):
        self.clear_screen()
        self.greet()
        self.initialize()
        while self.running:
            print("")
            print("---------------------------")
            v = input()
            self.evaluate_input(v)
        self.clear_screen()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
