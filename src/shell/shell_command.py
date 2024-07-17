import inspect
import subprocess
from abc import ABC, abstractmethod
from src.common import path

MAX_LBA_LEN = 100


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val

        if self.err:
            func = inspect.currentframe().f_back.f_back.f_code.co_name
            print(f"[ERR] error_code {self.err}, return_value {self.val} @{func}")


class ICommand(ABC):
    @abstractmethod
    def execute(self, *args) -> ReturnObject:
        pass

    def _system_call_ssd(self, operation, *args):
        print(f"python {path.SSD_EXEC} {operation} {' '.join(str(arg) for arg in args)}")
        self._ssd_sp = subprocess.run(f"python {path.SSD_EXEC} {operation} {' '.join(str(arg) for arg in args)}")


class WriteCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        # system call write
        self._system_call_ssd('W', *args)
        return ReturnObject(self._ssd_sp.returncode, None)


class ReadCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        # system call read
        self._system_call_ssd('R', *args)

        with open(path.DATA_FILE_RESULT, "r") as result_file:
            ret = result_file.readline()
            print(ret)

        return ReturnObject(self._ssd_sp.returncode, ret)


class EraseCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        # system call erase
        self._system_call_ssd('E', *args)
        return ReturnObject(self._ssd_sp.returncode, None)


class FullWriteCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        write_cmd = WriteCommand()
        for lba in range(MAX_LBA_LEN):
            ret = write_cmd.execute(lba, *args)
        return ret


class FullReadCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        read_cmd = ReadCommand()
        for lba in range(MAX_LBA_LEN):
            ret = read_cmd.execute(lba)
        return ret


class EraseRangeCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        erase_cmd = EraseCommand()
        ret = erase_cmd.execute(args[0], str(int(args[1]) - int(args[0])))
        return ret


class HelpCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        print("write [LBA] [VAL]  : write val on LBA(ex. write 3 0xAAAABBBB)")
        print("read [LBA]         : read val on LBA(ex. read 3)")
        print("erase [LBA] [SIZE] : erase val from LBA within size (ex. erase 3 5)")
        print("MAX SIZE: 10")
        print("exit               : exit program")
        print("help               : manual")
        print("fullwrite [VAL]    : write all val(ex. fullwrite 0xAAAABBBB")
        print("fullread           : read all val on LBA")
        print("erase_range [START_LBA] [END_LBA] : erase val from START_LBA to END_LBA size (ex. erase_rage 10 15)")

        return ReturnObject(0, None)


def create_shell_command(operation):
    if operation == 'write':
        return WriteCommand()
    elif operation == 'read':
        return ReadCommand()
    elif operation == 'erase':
        return EraseCommand()
    elif operation == 'fullwrite':
        return FullWriteCommand()
    elif operation == 'fullread':
        return FullReadCommand()
    elif operation == 'erase_range':
        return EraseRangeCommand()
    elif operation == 'help':
        return HelpCommand()
    else:
        print("[ERR] Invalid Command")
