# default
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

# local
from src.exception.exception_log import ExceptionLog
from src.ssd.hil import HostInterfaceLayer, OpCode


# DTO 랑 느낌이 비슷한데 그냥 Ssd를 HIL에 넘기는 방식으로 처리해도 될 듯...
class Ssd:
    def __init__(self):
        self.hil = HostInterfaceLayer()
        self.__op_code: OpCode
        self.__address: int
        self.__value: str
        self.__extra_commands: list
        self.args = []

    def set_hil(self, hil: HostInterfaceLayer):
        self.hil = hil

    def set_commands(self, command):
        self.__op_code = OpCode.get_op_code_by(command[1])
        self.__address = command[2]
        self.args.append(self.__address)
        if len(command) > 3:
            self.__value = command[3]
            self.__extra_commands = command[4:]

    def get_op_code(self):
        return self.__op_code

    def get_address(self):
        return self.__address

    def get_value(self):
        return self.__value

    def get_extra_commands(self):
        return self.__extra_commands

    # extra command는 무시한다.
    # ssd.py w 1 2 3 4 이렇게 넣어도 뒤에는 무시하고 ssd.py w 1 2로 해석하고 실행.
    def run(self):
        try:
            self.hil.get_command(self.__op_code, self.__address, self.__value)
        except:
            self.hil.get_command(self.__op_code, self.__address)


if __name__ == "__main__":
    commands = sys.argv
    ssd = Ssd()

    # 필요하다면 ssd에서 올라오는 exception을 다 잡아서 종류 별로 exit code 지정 가능
    # try:
    ssd.set_commands(commands)
    ssd.run()
    # except Exception as e:
    #     print(ExceptionLog.get_log_msg(e, "SSD Fail"))
    #     sys.exit(99)
