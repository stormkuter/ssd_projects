import subprocess
from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> int:
        pass


class WriteCommand(ICommand):
    def __init__(self, lba, val):
        self.__lba = lba
        self.__val = val

    def execute(self) -> int:
        # system call wrtie
        ssd_sp = subprocess.run(f"python -m ssd/hill.py w {self.__lba} {self.__val}")
        return ssd_sp.returncode


class ReadCommand(ICommand):
    pass


class FullWriteCommand(ICommand):
    pass


class FullCommand(ICommand):
    pass


class HelpCommand(ICommand):
    pass


def create_shell_command(opcode, *args):
    if opcode == 'write':
        return WriteCommand(*args)
    elif opcode == 'read':
        return ReadCommand(*args)
    elif opcode == 'fullwrite':
        return FullWriteCommand(*args)
    elif opcode == 'fullread':
        return FullCommand(*args)
    elif opcode == 'help':
        return HelpCommand(*args)
    else:
        print("INVALID COMMAND")
