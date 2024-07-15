import enum
from src.ssd.fil import FlashInterfaceLayer


class OpCode(enum.Enum):
    READ = 0
    WRITE = 1

    @classmethod
    def get_op_code_by(cls, command: str):
        if command == "R":
            return OpCode.READ
        if command == "W":
            return OpCode.WRITE
        else:
            raise ValueError(f"잘못된 명령어가 입력되었습니다.: {command}")


class HostInterfaceLayer:
    def __init__(self):
        self.__fil = FlashInterfaceLayer()

    def set_fil(self, fil: FlashInterfaceLayer):
        self.__fil = fil

    def get_command(self, command: str, *args, **kwargs):
        op_code = OpCode.get_op_code_by(command)
        self.__validation_of_address(args[0])
        if op_code == OpCode.READ:
            self.__fil.read_lba(args[0])
        elif op_code == OpCode.WRITE:
            self.__validation_of_value(args[1])
            self.__fil.write_lba(args[0], args[1])

    def __validation_of_address(self, address):
        if not isinstance(address, int) or (0 >= address) or (address >= 100):
            raise ValueError("입력된 주소값이 잘못 되었습니다.")

    def __validation_of_value(self, value):
        print(value, type(value))
        min_4byte = 0
        max_4byte = 2 ** 32 - 1
        if not isinstance(value, int) or (min_4byte >= value) or (value >= max_4byte):
            raise ValueError("입력된 값이 잘못 되었습니다.")
