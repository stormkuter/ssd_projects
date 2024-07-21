# default
import os
import sys

from src.common.path import RUNNER_MODE_FILE

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

# local
from src.common.logger import LOGGER
from src.ssd.op_code import OpCode
from src.ssd.ssd_command import SsdCommand, SsdReadCommand, SsdWriteCommand, SsdEraseCommand, SsdFlushCommand


class Ssd:
    def __init__(self):
        self.command: SsdCommand
        self.operation_code = None

    def set_on_command(self, command: SsdCommand):
        self.command = command

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
            self.set_on_command(SsdWriteCommand(commands[2], commands[3]))

        if self.operation_code == OpCode.ERASE:
            self.validate_erase_arg(commands)
            self.set_on_command(SsdEraseCommand(commands[2], commands[3]))

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
    if os.path.exists(RUNNER_MODE_FILE):
        LOGGER.setup_handler(True)

    try:
        ssd = Ssd()
        ssd.parse_commands(commands)
        ssd.command.execute()

    except Exception as e:
        LOGGER.debug(str(e))
        sys.exit(99)
