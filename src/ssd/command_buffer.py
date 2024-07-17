import json
import os

from src.common.path import *
from src.ssd.hil import OpCode

INIT_BUFFER_DATA = {"commands": [], "tempStorage": [[] for _ in range(100)]}
ERASE_VALUE = "-1"
EMPTY_VALUE = "0x00000000"
COMMAND_LIMIT = 10

class CommandBuffer:
    def __init__(self):
        self.buffer_data = INIT_BUFFER_DATA
        self.commands_to_return = None
        self.__read_buffer_file()

    def __read_buffer_file(self):
        self.initialize_file()
        with open(DATA_FILE_BUFFER, "r") as file:
            self.buffer_data = json.load(file)

    def initialize_file(self):
        if not os.path.exists(SOURCE_BASE_DIR):
            os.mkdir(SOURCE_BASE_DIR)
        if not os.path.exists(DATA_FILE_BUFFER):
            with open(DATA_FILE_BUFFER, "w") as file:
                json.dump(INIT_BUFFER_DATA, file, ensure_ascii=False, indent=4)

    def update_file(self):
        # self.buffer_data["commands"].append(["W", "1", "0xFFFFFFFF"])
        # self.buffer_data["tempStorage"][0] = ['0xFFFFFFFF']
        with open(DATA_FILE_BUFFER, "w") as file:
            json.dump(self.buffer_data, file, ensure_ascii=False, indent=4)

    # TODO:: Refactoring 필수 대상 2222
    def execute(self, *args):
        op_code = args[0]
        if op_code == OpCode.READ:
            lba = args[1]
            if self.is_value_present():
                return self.get_last_value(lba)
            else:
                raise ValueError

        command = op_code.value

        if op_code == OpCode.WRITE:
            lba, value = args[1:3]
            self.add_command(command, lba, value)
            self.update_temp_storage(lba, value)

        if op_code == OpCode.ERASE:
            start_lba, end_lba = args[1:3]
            self.add_command(command, start_lba, end_lba)
            for lba in range(int(start_lba, int(end_lba))):
                self.update_temp_storage(str(lba), ERASE_VALUE)

        if op_code == OpCode.FLUSH:
            self.flush()
            return self.get_commands_requiring_save()

    def add_command(self, *args):
        self.buffer_data["commands"].append([x for x in args])

    def update_temp_storage(self, lba: str, value: str):
        self.buffer_data["tempStorage"][int(lba)].append(value)

    def is_value_present(self, lba: str):
        return len(self.buffer_data["tempStorage"][int(lba)]) > 0

    def get_last_value(self, lba: str):
        last_value = self.buffer_data["tempStorage"][int(lba)][-1]
        if last_value == ERASE_VALUE:
            return EMPTY_VALUE
        else:
            return last_value

    def is_full_commands(self):
        return len(self.buffer_data["commands"]) >= 10


    # TODO:: Refactoring 필수 대상
    def flush(self):
        self.commands_to_return = self.buffer_data["commands"]
        temp_command_list = []
        for lba in range(100):
            if len(self.buffer_data["tempStorage"][lba]) == 0:
                continue
            last_value = self.buffer_data["tempStorage"][lba][-1]

            if len(temp_command_list) == 0:
                if last_value == ERASE_VALUE:
                    temp_command_list.append([OpCode.ERASE.value, str(lba), 1])
                else:
                    temp_command_list.append([OpCode.WRITE.value, str(lba), last_value])

            elif last_value == ERASE_VALUE:
                if temp_command_list[-1][0] == OpCode.ERASE.value:
                    temp_command_list[-1][2] += 1
                else:
                    temp_command_list.append([OpCode.ERASE.value, str(lba), 1])
            else:
                temp_command_list.append([OpCode.WRITE.value, str(lba), last_value])

        self.commands_to_return = min(self.commands_to_return,temp_command_list)
        self.buffer_data = INIT_BUFFER_DATA

    def get_commands_requiring_save(self):
        return self.commands_to_return