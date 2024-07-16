# default
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

# local
from src.ssd.hil import HostInterfaceLayer, OpCode


class Ssd:
    def __init__(self):
        self.hil = HostInterfaceLayer()
        self.__op_code: OpCode
        self.__extra_commands: list

    def set_hil(self, hil: HostInterfaceLayer):
        self.hil = hil

    def set_commands(self, command):
        self.__op_code = OpCode.get_op_code_by(command[1])
        self.__extra_commands = command[2:]

    def get_op_code(self):
        return self.__op_code

    def get_extra_commands(self):
        return self.__extra_commands

    def run(self):
        self.hil.get_command(self.__op_code, self.__extra_commands)


if __name__ == "__main__":
    commands = sys.argv
    ssd = Ssd()
    ssd.set_commands(commands)

    # 필요하다면 ssd에서 올라오는 exception을 다 잡아서 종류 별로 exit code 지정하는 것으로...
    try:
        ssd.run()
    except:
        sys.exit(99)
