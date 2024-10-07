from typing import List

from terminal.argument import Argument, Command
from terminal.argument_definition import CommandDefinition


class Parser:
    commands: List[CommandDefinition]

    def __init__(self):
        self.commands = []

    def add_command_definition(self, command: CommandDefinition):
        self.commands.append(command)
        return self

    def parse(self, input: str):
        input_list = str_to_list(input)

        if len(input_list) == 0:
            print("invalid command")
            return

        command_def = self.get_first_matching_command(input_list[0])

        if command_def is None:
            return

        arguments = []
        if len(input_list) > 1:
            arguments = self.parse_arguments(input_list[1:], command_def)

        command = Command(command_def.command)

        for a in arguments:
            command.add_argument(a)

        return command

    def get_first_matching_command(self, command: str):
        for c in self.commands:
            if c.command == command:
                return c
        return None

    def parse_arguments(self, args: List[str], command_def: CommandDefinition):
        arguments = []
        for i in range(len(args)):
            for a in command_def.arguments:
                if args[i] == a.argument:
                    value = ""
                    if a.argument_has_value() and (i + 1) < len(args):
                        i += 1
                        value = args[i]
                    argument = Argument(a.name, value, a.type)
                    arguments.append(argument)
        return arguments


def str_to_list(input: str) -> List[str]:
    return input.split(" ")
