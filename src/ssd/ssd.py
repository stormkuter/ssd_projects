# default
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

# local
from src.ssd.op_code import OpCode
from src.ssd.ssd_command import SsdCommand, SsdReadCommand, SsdWriteCommand, SsdEraseCommand, SsdFlushCommand
from src.ssd.fil import FlashInterfaceLayer
from src.ssd.hil import HostInterfaceLayer
from src.ssd.command_buffer import CommandBuffer
from src.exception.exception_log import ExceptionLog

# DTO 랑 느낌이 비슷한데 그냥 Ssd를 HIL에 넘기는 방식으로 처리해도 될 듯...
class Ssd:
    def __init__(self):
        self.hil = None
        self.__op_code = None
        self.__address = None
        self.__value = None
        # 커멘드 패턴 용
        self.command: SsdCommand
        self.operation_code = None

    def set_hil(self, hil: HostInterfaceLayer):
        self.hil = hil

    def set_commands(self, command):
        self.__op_code = command[1]
        if len(command) > 2:
            self.__address = command[2]
        if len(command) > 3:
            self.__value = command[3]

    def get_op_code(self):
        return self.__op_code

    def get_address(self):
        return self.__address

    def get_value(self):
        return self.__value

    # extra command는 무시한다.
    # ssd.py w 1 2 3 4 이렇게 넣어도 뒤에는 무시하고 ssd.py w 1 2로 해석하고 실행.
    def run(self):
        if self.__value is not None:
            self.hil.execute(self.__op_code, self.__address, self.__value)
        elif self.__address is not None:
            self.hil.execute(self.__op_code, self.__address)
        else:
            self.hil.execute(self.__op_code)

    def set_on_command(self, command: SsdCommand):
        self.command = command

    def run_command(self):
        self.command.execute()

    def parse_commands(self, commands):
        if len(commands) == 1:
            raise ValueError("W/R/F/E 명령이 없어요")
        command = commands[1]
        self.operation_code = OpCode.get_op_code_by(command)
        if self.operation_code == OpCode.READ:
            self.validate_read_arg(commands)
            self.set_on_command(SsdReadCommand(commands[2]))

        if self.operation_code == OpCode.WRITE:
            self.validate_write_arg(commands)
            self.set_on_command(SsdWriteCommand(commands[3], commands[4]))

        if self.operation_code == OpCode.WRITE:
            self.validate_erase_arg(commands)
            self.set_on_command(SsdEraseCommand(commands[3], commands[4]))

        if self.operation_code == OpCode.FLUSH:
            self.validate_flush_arg(commands)
            self.set_on_command(SsdFlushCommand())

    def validate_read_arg(self, commands):
        if len(commands[2:]) != 1:
            raise ValueError("READ는 매개 변수 1개")

    def validate_write_arg(self, commands):
        if len(commands[2:]) != 2:
            raise ValueError("WRITE는 매개 변수 2개")

    def validate_erase_arg(self, commands):
        if len(commands[2:]) != 2:
            raise ValueError("ERASE는 매개 변수 2개")
    def validate_flush_arg(self, commands):
        if len(commands) != 2:
            raise ValueError("FLUSH는 매개 변수 0개")




if __name__ == "__main__":
    commands = sys.argv
    print(commands)
    # ssd = Ssd()
    # hil = HostInterfaceLayer(CommandBuffer())
    # hil.set_fil(FlashInterfaceLayer())
    # ssd.set_hil(hil)

    # 필요하다면 ssd에서 올라오는 exception을 다 잡아서 종류 별로 exit code 지정 가능
    # try:
    # ssd.set_commands(commands)
    # ssd.run()
    # except Exception as e:
    #     print(ExceptionLog.get_log_msg(e, "SSD Fail"))
    #     sys.exit(99)


    ## 커멘드 페턴 용
    ssd = Ssd()
    ssd.parse_commands(commands)
    ssd.command.execute()
