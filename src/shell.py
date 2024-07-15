from ssd.hil import HostInterfaceLayer, OpCode


class Shell:
    def __init__(self):
        self.__ssd = HostInterfaceLayer()

    def command(self):
        # if input() == "ssd W 2 0xAAAABBBB"
        self.__ssd.get_command(OpCode.WRITE, 2, 0xAAAABBBB)
        pass


if __name__ == "__main__":
    shell = Shell()
