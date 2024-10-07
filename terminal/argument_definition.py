from typing import List

from terminal.argument_type import ArgumentType


class ArgDefinition:
    argument: str
    name: str
    description: str
    type: ArgumentType

    def __init__(self, argument: str, name: str, description: str, type: ArgumentType):
        self.argument = argument
        self.description = description
        self.name = name
        self.type = type

    def argument_has_value(self):
        arg_with_values = [
            ArgumentType.TYPE_DIMENSION.value,
            ArgumentType.TYPE_FLOAT.value,
            ArgumentType.TYPE_INT.value,
            ArgumentType.TYPE_STR.value,
        ]
        if self.type.value in arg_with_values:
            return True
        return False


class CommandDefinition:
    command: str
    description: str
    arguments: List[ArgDefinition]

    def __init__(self, command: str, description: str):
        self.command = command
        self.description = description
        self.arguments = []

    def add_argument_definition(self, argument: ArgDefinition):
        self.arguments.append(argument)
        return self
