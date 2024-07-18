from abc import ABC, abstractmethod

from src.common.path import DATA_FILE_RESULT
from src.ssd.command_buffer import CommandBuffer
from src.ssd.fil import FlashInterfaceLayer
from src.ssd.op_code import OpCode


class SsdCommand(ABC):
    def __init__(self):
        self.fil = None
        self.command_buffer = None
        self.MIN_VALUE = 0
        self.MAX_VALUE = 2 ** 32 - 1
        self.MIN_ADDRESS = 0
        self.MAX_ADDRESS = 99
        self.EMPTY_VALUE = "0x00000000"
        self.fil = FlashInterfaceLayer()
        self.command_buffer = CommandBuffer()

    def set_fil(self, fil: FlashInterfaceLayer):
        self.fil = fil

    def set_command_buffer(self, command_buffer: CommandBuffer):
        self.command_buffer = command_buffer

    def flush(self):
        self.command_buffer.flush()
        self.command_buffer.update_file()
        command_list = self.command_buffer.get_commands_requiring_save()
        self.excute_command_list(command_list)


    def excute_command_list(self, command_list: list):
        for command in command_list:
            op_code = OpCode.get_op_code_by(command[0])
            if op_code == OpCode.WRITE:
                self.write(command[1], command[2])
            elif op_code == OpCode.ERASE:
                self.erase(command[1], command[2])
            elif op_code == OpCode.READ:
                self.read(command[1])

    def write(self, lba: str, value: str):
        self.fil.write_lba(lba, value)

    def read(self, lba: str, value: str):
        self.fil.write_lba(lba, self.to_upper(value))

    def erase(self, start_lba: str, size: str):
        self.fil.erase_lba(start_lba, size)

    def to_upper(self, value: str):
        return value[:2] + value[2:].upper()

    def validation_of_lba(self, lba: str):
        if lba[:2] == "0x":
            try:
                lba = int(lba, 16)
            except:
                raise ValueError(f"입력된 주소값이 잘못 되었습니다.: {lba}")
        elif lba.isdigit():
            lba = int(lba)
        else:
            raise ValueError(f"입력된 주소값이 잘못 되었습니다.: {lba}")

        if (self.MIN_ADDRESS > lba) or (lba > self.MAX_ADDRESS):
            raise ValueError(f"입력된 주소값이 범위를 벗어났습니다.: {lba}")

    def validation_of_value(self, value: str):
        if len(value) == 10:
            try:
                value = int(value, 16)
            except:
                raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.: {value}")
        else:
            raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.: {value}")

        if (self.MIN_VALUE > value) or (value > self.MAX_VALUE):
            raise ValueError(f"입력된 값이 잘못 되었습니다.: {value}")

    def validation_of_size(self, size: str):
        if not size.isdigit():
            raise ValueError(f"입력된 값이 잘못 되었습니다.: {size}")
        if 1 > int(size) or int(size) > 10:
            raise ValueError(f"입력된 값이 범위를 벗어났습니다.: {size}")

    @abstractmethod
    def execute(self):
        pass



class SsdReadCommand(SsdCommand):
    def __init__(self, lba: str):
        super().__init__()
        self.lba = lba

    def execute(self):
        self.validate_args()
        if self.command_buffer.is_value_present(self.lba):
            read_value = self.command_buffer.get_last_value(self.lba)
            with open(DATA_FILE_RESULT, "w") as f:
                f.write(read_value)
        else:
            self.fil.read_lba(self.lba)

    def validate_args(self):
        self.validation_of_lba(self.lba)


class SsdWriteCommand(SsdCommand):
    def __init__(self, lba: str, value: str):
        super().__init__()
        self.lba = lba
        self.value = value

    def execute(self):
        self.validate_args()
        self.value = self.value[:2] + self.value[2:].upper()
        if self.command_buffer.is_full_commands():
            self.flush()
        self.command_buffer.add_command("W", self.lba, self.value)
        self.command_buffer.update_temp_storage(self.lba, self.value)
        self.command_buffer.update_file()

    def validate_args(self):
        self.validation_of_lba(self.lba)
        self.validation_of_value(self.value)


class SsdEraseCommand(SsdCommand):
    def __init__(self, lba: str, size: str):
        super().__init__()
        self.ERASE_VALUE = "-1"
        self.ERASE_CODE = "E"
        self.lba = lba
        self.size = size

    def execute(self):
        self.validate_args()
        if self.command_buffer.is_full_commands():
            self.flush()
        self.command_buffer.add_command(self.ERASE_CODE, self.lba, self.size)
        start_lba = int(self.lba)
        end_lba = int(self.lba) + int(self.size)
        for lba in range(start_lba, end_lba):
            self.command_buffer.update_temp_storage(str(lba), self.ERASE_VALUE)
        self.command_buffer.update_file()

    def validate_args(self):
        self.validation_of_lba(self.lba)
        self.validation_of_lba(self.size)


class SsdFlushCommand(SsdCommand):
    def __init__(self):
        super().__init__()

    def execute(self):
        self.flush()
