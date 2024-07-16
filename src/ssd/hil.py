import enum
from src.ssd.fil import FlashInterfaceLayer

MIN_VALUE = 0
MAX_VALUE = 2 ** 32 - 1
MIN_ADDRESS = 0
MAX_ADDRESS = 99


class OpCode(enum.Enum):
    READ = 0
    WRITE = 1

    @classmethod
    def get_op_code_by(cls, command: str):
        command = command.lower()
        if command == "r":
            return OpCode.READ
        if command == "w":
            return OpCode.WRITE
        else:
            raise ValueError(f"잘못된 명령어가 입력되었습니다.: {command}")


class HostInterfaceLayer:

    def __init__(self):
        self.__fil = FlashInterfaceLayer()

    def set_fil(self, fil: FlashInterfaceLayer):
        self.__fil = fil

    def get_command(self, op_code: OpCode, *args, **kwargs):
        self.__validation_args(args)
        if op_code == OpCode.READ:
            self.__fil.read_lba(args[0])
        elif op_code == OpCode.WRITE:
            self.__fil.write_lba(args[0], args[1])

    def __validation_args(self, args):
        if len(args) == 0:
            raise ValueError("입력 주소 및 값이 없습니다.")
        self.__validation_of_address(args[0])

        if len(args) == 2:
            self.__validation_of_value(args[1])

    def __validation_of_address(self, address):
        if not isinstance(address, str) or (MIN_ADDRESS > int(address)) or (int(address) > MAX_ADDRESS):
            raise ValueError(f"입력된 주소값이 잘못 되었습니다.: {address}")

    def __validation_of_value(self, value: str):
        if len(value) != 10 or value[:2] != "0x":
            raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.: {value}")
        result_value = 0
        for i in range(2, 10):
            result_value += self.__to_int(value[i]) * 16 ** (9-i)
        if (MIN_VALUE > result_value) or (result_value > MAX_VALUE):
            raise ValueError(f"입력된 값이 잘못 되었습니다.: {value}")

    def __to_int(self, spell: str):
        spell_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
        if spell.isdigit():
            return int(spell)
        elif spell.upper() in spell_dict:
            return spell_dict[spell.upper()]
        else:
            raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.")
