import os
from src.shell.shell_command import create_shell_command


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val


class TestAppBase:
    def __init__(self):
        self.__write = create_shell_command("write")
        self.__read = create_shell_command("read")
        self.__full_write = create_shell_command("fullwrite")
        self.__full_read = create_shell_command("fullread")
        self.__flush = create_shell_command("flush")
        self.__erase = create_shell_command("erase")
        self.__erase_range = create_shell_command("erase_range")
        self.__set_up()

    def __del__(self):
        self.__tear_down()

    def __set_up(self):
        self.flush()

    def __tear_down(self):
        self.flush()

    def write(self, lba, value):
        return self.__write.execute(lba, value)

    def read(self, lba):
        return self.__read.execute(lba)

    def full_write(self, value):
        return self.__full_write.execute(value).val

    def full_read(self):
        return self.__full_read.execute()

    def flush(self):
        return self.__flush.execute()

    def erase(self, start_lba, number_of_logical_blocks):
        return self.__erase.execute(start_lba, number_of_logical_blocks)

    def erase_range(self, start_lba, end_lba):
        return self.__erase_range.execute(start_lba, end_lba)


def list_modules():
    package_path = os.path.dirname(__file__)
    module_list = []

    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = os.path.splitext(file)[0]
                relative_path = os.path.relpath(root, package_path).replace(os.sep, '.')
                if relative_path == ".":
                    module_list.append(module_name)
                else:
                    module_list.append(f"{relative_path}.{module_name}")

    return module_list


__all__ = list_modules()
