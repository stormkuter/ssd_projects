import enum
from fil import FlashInterfaceLayer


class OpCode(enum.Enum):
    READ = 0
    WRITE = 1


class HostInterfaceLayer:
    def __init__(self):
        self.__fil = FlashInterfaceLayer()

    def get_command(self, op_code, *args, **kwargs):
        if op_code == OpCode.READ:
            self.__fil.read_lba(args[0])
        elif op_code == OpCode.WRITE:
            self.__fil.write_lba(args[0], args[1])
        pass
