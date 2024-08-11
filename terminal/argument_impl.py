from terminal.argument_type import ArgumentType
from typing import List
import terminal.argument_validator as arg_validator

class Argument:
    argument: str
    value: str
    type: ArgumentType

    def __init__(self, argument: str, value:str, type: ArgumentType):
        self.argument = argument
        self.value = value
        self.type = type

class Command:
    command: str
    arguments: List[Argument]

    def __init__(self, command: str):
        self.command = command
        self.arguments = []
    
    def add_argument(self, argument: Argument):
        self.arguments.append(argument)
        return self
    
    def has_argument(self, arg: str):
        return arg in [a.argument for a in self.arguments]
    
    def get_argument(self, arg: str):
        if not self.has_argument(arg):
            return None
        for a in self.arguments:
            if a.argument == arg:
                return a
        return None

    def arguments_are_valid(self):
        args_are_valid = True
        for arg in self.arguments:
            if arg.type.value == ArgumentType.TYPE_INT.value:
                if not arg_validator.is_valid_int(arg.value):
                    args_are_valid = False
                    break
            if arg.type.value == ArgumentType.TYPE_DIMENSION.value:
                if not arg_validator.is_valid_dimension(arg.value):
                    args_are_valid = False
                    break
            if arg.type.value == ArgumentType.TYPE_FLOAT.value:
                if not arg_validator.is_valid_float(arg.value):
                    args_are_valid = False
                    break
            if arg.type.value == ArgumentType.TYPE_STR.value:
                if not arg_validator.is_valid_str(arg.value):
                    args_are_valid = False
                    break
        return args_are_valid