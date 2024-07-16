import subprocess
from abc import ABC, abstractmethod
from src.common import path

MAX_LBA_LEN = 100


class ICommand(ABC):
    @abstractmethod
    def execute(self, *args) -> (int, str):
        pass


class WriteCommand(ICommand):
    def execute(self, lba, val) -> (int, str):
        # system call write
        ssd_sp = subprocess.run(f"python {path.SSD_EXEC} W {lba} {val}")
        return (ssd_sp.returncode, None)


class ReadCommand(ICommand):
    def execute(self, lba) -> (int, str):
        # system call read
        ssd_sp = subprocess.run(f"python {path.SSD_EXEC} R {lba}")
        result_file = open(path.DATA_FILE_RESULT, "r")
        ret = result_file.readline()
        print(ret)
        result_file.close()

        return (ssd_sp.returncode, ret)


class FullWriteCommand(ICommand):
    def execute(self, val) -> (int, str):
        # system call full wrtie
        for lba in range(MAX_LBA_LEN):
            ssd_sp = subprocess.run(f"python {path.SSD_EXEC} W {lba} {val}")
            if ssd_sp == -1:
                return ssd_sp.returncode, None
        return ssd_sp.returncode, None


class FullReadCommand(ICommand):
    def execute(self) -> (int, str):
        # system call full read
        for lba in range(MAX_LBA_LEN):
            ssd_sp = subprocess.run(f"python {path.SSD_EXEC} R {lba}")
            if ssd_sp == -1:
                return ssd_sp.returncode, None
            result_file = open(path.DATA_FILE_RESULT, "r")
            ret = result_file.readline()
            print(ret)
            result_file.close()
        return ssd_sp.returncode, None


def create_shell_command(opcode):
    if opcode == 'write':
        return WriteCommand()
    elif opcode == 'read':
        return ReadCommand()
    elif opcode == 'fullwrite':
        return FullWriteCommand()
    elif opcode == 'fullread':
        return FullReadCommand()
    else:
        print("INVALID COMMAND")
