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

    def get_command(self, op_code, *args, **kwargs):
        if op_code == OpCode.READ:
            self.__fil.read_lba(args[0])
        elif op_code == OpCode.WRITE:
            self.__fil.write_lba(args[0], args[1])
        pass
