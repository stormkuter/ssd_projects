import inspect
from src.shell.shell_command import create_shell_command


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val


class ShellOperation:
    def __init__(self):
        self.__write = create_shell_command("write")
        self.__read = create_shell_command("read")
        self.__full_write = create_shell_command("fullwrite")
        self.__full_read = create_shell_command("fullread")

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

    def test_app_1(self, value):
        pass

    def test_app_2(self):
        pass

    def help(self):
        print("write [LBA] [VAL]  : write val on LBA(ex. write 3 0xAAAABBBB)")
        print("read [LBA]         : read val on LBA(ex. read 3)")
        print("exit               : exit program")
        print("help               : manual")
        print("fullwrite [VAL]    : write all val(ex. fullwrite 0xAAAABBBB")
        print("fullread           : read all val on LBA")
