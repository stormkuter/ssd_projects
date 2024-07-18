import inspect
import subprocess
from abc import ABC, abstractmethod
from src.common import path
from src.common.logger import LOGGER
from src.common.ssd_config import NUM_LBAS, MAX_ERASE_SIZE, MIN_LBA


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val

        if self.err:
            func = inspect.currentframe().f_back.f_back.f_code.co_name
            LOGGER.debug(f"[ERR] error_code {self.err}, return_value {self.val} @{func}")


class ICommand(ABC):
    @abstractmethod
    def execute(self, *args) -> ReturnObject:
        pass

    def _system_call_ssd(self, operation, *args):
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

        if not self._ssd_sp.returncode:
            LOGGER.debug(ret)

        return ReturnObject(self._ssd_sp.returncode, ret)


class EraseCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        # system call erase
        lba, size = int(args[0]), int(args[1])

        if lba < MIN_LBA: return ReturnObject(-1, None)
        if size > NUM_LBAS: return ReturnObject(-1, None)

        while size > MAX_ERASE_SIZE:
            self._system_call_ssd('E', lba, MAX_ERASE_SIZE)
            size -= MAX_ERASE_SIZE
            lba += MAX_ERASE_SIZE
        self._system_call_ssd('E', lba, size)

        return ReturnObject(self._ssd_sp.returncode, None)


class FlushCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        # system call flush
        self._system_call_ssd('F', *args)
        return ReturnObject(self._ssd_sp.returncode, None)


class FullWriteCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        ret = ReturnObject(0, None)

        write_cmd = WriteCommand()
        for lba in range(NUM_LBAS):
            write_ret = write_cmd.execute(lba, *args)
            if write_ret.err: ret = write_ret

        return ret


class FullReadCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        ret = ReturnObject(0, None)

        read_cmd = ReadCommand()
        for lba in range(NUM_LBAS):
            read_ret = read_cmd.execute(lba)
            if read_ret.err: ret = read_ret

        if ret.err: return ret
        return ReturnObject(0, read_ret.val)


class EraseRangeCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        erase_cmd = EraseCommand()
        try:
            lba = args[0]
            size = str(int(args[1]) - int(args[0]))
        except Exception as e:
            return ReturnObject(-1, None)

        return erase_cmd.execute(lba, size)


class HelpCommand(ICommand):
    def execute(self, *args) -> ReturnObject:
        LOGGER.debug("write [LBA] [VAL]  : write val on LBA(ex. write 3 0xAAAABBBB)")
        LOGGER.debug("read [LBA]         : read val on LBA(ex. read 3)")
        LOGGER.debug("erase [LBA] [SIZE] : erase val from LBA within size (ex. erase 3 5)")
        LOGGER.debug("MAX SIZE: 10")
        LOGGER.debug("flush              : flush current buffer")
        LOGGER.debug("exit               : exit program")
        LOGGER.debug("help               : manual")
        LOGGER.debug("fullwrite [VAL]    : write all val(ex. fullwrite 0xAAAABBBB")
        LOGGER.debug("fullread           : read all val on LBA")
        LOGGER.debug(
            "erase_range [START_LBA] [END_LBA] : erase val from START_LBA to END_LBA size (ex. erase_rage 10 15)")

        return ReturnObject(0, None)


def create_shell_command(operation):
    if operation == 'write':
        return WriteCommand()
    elif operation == 'read':
        return ReadCommand()
    elif operation == 'erase':
        return EraseCommand()
    elif operation == 'flush':
        return FlushCommand()
    elif operation == 'fullwrite':
        return FullWriteCommand()
    elif operation == 'fullread':
        return FullReadCommand()
    elif operation == 'erase_range':
        return EraseRangeCommand()
    elif operation == 'help':
        return HelpCommand()

    raise Exception("Invalid Command Exception")
