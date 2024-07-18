import os
import random
from src.common import ssd_config
from src.common.logger import LOGGER
from src.shell.shell_command import create_shell_command


class ReturnObject:
    def __init__(self, err, val):
        self.err = err
        self.val = val


class TestAppBase:
    def __init__(self, random_seed=None):
        self.__write = create_shell_command("write")
        self.__read = create_shell_command("read")
        self.__full_write = create_shell_command("fullwrite")
        self.__full_read = create_shell_command("fullread")
        self.__flush = create_shell_command("flush")
        self.__erase = create_shell_command("erase")
        self.__erase_range = create_shell_command("erase_range")

        if not random_seed:
            random_seed = random.randint(0, 100)

        LOGGER.debug(f"======== Start Test (Seed: {random_seed}) ========")
        random.seed(random_seed)

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

    def get_random_lba(self, start_lba=ssd_config.MIN_LBA, end_lba=ssd_config.MAX_LBA):
        return random.randrange(start_lba, end_lba + 1)

    def get_random_lba_range(self, size=ssd_config.COMMAND_BUFFER_SIZE):
        start_lba = random.randint(ssd_config.MIN_LBA, ssd_config.MAX_LBA - size + 1)
        end_lba = start_lba + size - 1
        return [start_lba, end_lba]

    def get_random_value(self, min_value=ssd_config.MIN_VALUE, max_value=ssd_config.MAX_VALUE):
        value = random.randrange(min_value, max_value + 1)
        value_str = "0x" + hex(value)[2:].zfill(8).upper()
        return value_str


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
