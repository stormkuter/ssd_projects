import subprocess
from abc import ABC, abstractmethod

MAX_LBA_LEN = 100


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> int:
        pass


class WriteCommand(ICommand):
    def __init__(self, lba, val):
        self.__lba = lba
        self.__val = val

    def execute(self) -> int:
        # system call write
        ssd_sp = subprocess.run(f"python -m ssd/hill.py W {self.__lba} {self.__val}")
        return ssd_sp.returncode


class ReadCommand(ICommand):
    def __init__(self, lba):
        self.__lba = lba

    def execute(self) -> int:
        # system call read
        ssd_sp = subprocess.run(f"python -m ssd/hill.py R {self.__lba}")
        result_file = open("result.txt", "r")
        ret = result_file.readline()
        print(ret)
        result_file.close()

        return ssd_sp.returncode


class FullWriteCommand(ICommand):
    def __init__(self, val):
        self.__val = val

    def execute(self) -> int:
        # system call full wrtie
        for lba in range(MAX_LBA_LEN):
            ssd_sp = subprocess.run(f"python -m ssd/hill.py W {lba} {self.__val}")
            if ssd_sp == -1:
                return -1
        return 0


class FullReadCommand(ICommand):
    def __init__(self):
        super().__init__()

    def execute(self) -> int:
        # system call full read
        for lba in range(MAX_LBA_LEN):
            ssd_sp = subprocess.run(f"python -m ssd/hill.py R {lba}")
            if ssd_sp == -1:
                return -1
            result_file = open("result.txt", "r")
            ret = result_file.readline()
            print(ret)
            result_file.close()
        return 0


def create_shell_command(opcode, *args):
    if opcode == 'write':
        return WriteCommand(*args)
    elif opcode == 'read':
        return ReadCommand(*args)
    elif opcode == 'fullwrite':
        return FullWriteCommand(*args)
    elif opcode == 'fullread':
        return FullReadCommand()
    else:
        print("INVALID COMMAND")
