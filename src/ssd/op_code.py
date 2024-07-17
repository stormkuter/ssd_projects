import enum


class OpCode(enum.Enum):
    READ = "R"
    WRITE = "W"
    ERASE = "E"
    FLUSH = "F"

    @classmethod
    def get_op_code_by(cls, command: str):
        command = command.upper()
        for op_code in OpCode:
            if op_code.value == command:
                return op_code
        raise ValueError(f"잘못된 명령어가 입력되었습니다.: {command}")
