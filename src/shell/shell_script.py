import inspect
from src.shell.shell_command import WriteCmdFactory, ReadCmdFactory, FullWriteCmdFactory, \
    FullReadCmdFactory

NUM_LBAS = 100


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val


class ShellOperation:
    def __init__(self):
        self.__write = WriteCmdFactory().createCommand()
        self.__read = ReadCmdFactory().createCommand()
        self.__full_write = FullWriteCmdFactory().createCommand()
        self.__full_read = FullReadCmdFactory().createCommand()

    def __handle_error(self, result):
        ret = ReturnObject(result[0], result[1])
        if ret.err:
            func = inspect.currentframe().f_back.f_back.f_code.co_name
            print(f"[ERR] error_code {ret.err}, return_value {ret.val} @{func}")
        return ret

    def write(self, lba, value):
        return self.__handle_error(self.__write.execute(lba, value))

    def read(self, lba):
        return self.__handle_error(self.__read.execute(lba))

    def full_write(self, value):
        return self.__handle_error(self.__full_write.execute(value))

    def full_read(self):
        return self.__handle_error(self.__full_read.execute())

    def test_app_1(self, expected="0x12345678"):
        is_mismatched = False
        self.full_write(expected)
        for lba in range(NUM_LBAS):
            read_value = self.read(lba).val
            if read_value != expected:
                print(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            print("Data is written well")

    def test_app_2(self):
        is_mismatched = False
        deprecated = "0xAAAABBBB"
        expected = "0x12345678"

        for i in range(30):
            for lba in range(0, 6):
                self.write(lba, deprecated)

        for lba in range(0, 6):
            self.write(lba, expected)

        for lba in range(0, 6):
            read_value = self.read(lba).val
            if read_value != expected:
                print(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            print("Data is written well")

    def help(self):
        print("write [LBA] [VAL]  : write val on LBA(ex. write 3 0xAAAABBBB)")
        print("read [LBA]         : read val on LBA(ex. read 3)")
        print("exit               : exit program")
        print("help               : manual")
        print("fullwrite [VAL]    : write all val(ex. fullwrite 0xAAAABBBB")
        print("fullread           : read all val on LBA")
