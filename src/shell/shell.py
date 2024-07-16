from src.shell.shell_command import create_shell_command


class Shell:

    def __init__(self):
        self.__command = None

    def write(self, lba, val) -> int:
        self.__command = create_shell_command('write')
        return_code = self.__command.execute(lba, val)

        if not return_code == 0:
            pass

        return return_code

    def read(self, lba):
        self.__command = create_shell_command('read')
        return_code = self.__command.execute(lba)

        if not return_code == 0:
            pass

        return return_code

    def help(self):
        print("write [LBA] [VAL]  : write val on LBA(ex. write 3 0xAAAABBBB)")
        print("read [LBA]         : read val on LBA(ex. read 3)")
        print("exit               : exit program")
        print("help               : manual")
        print("fullwrite [VAL]    : write all val(ex. fullwrite 0xAAAABBBB")
        print("fullread           : read all val on LBA")

    def full_write(self, val):
        self.__command = create_shell_command('fullwrite')
        return_code = self.__command.execute(val)

        if not return_code == 0:
            pass

        return return_code

    def full_read(self):
        self.__command = create_shell_command('fullread')
        return_code = self.__command.execute()

        if not return_code == 0:
            pass

        return return_code

    def run(self):
        print('================= SSD Shell Started! =================')
        while True:
            user_input = input(">> ").strip()
            args = user_input.split()

            if args[0] == 'write':
                self.write(args[1], args[2])
            elif args[0] == 'read':
                self.read(args[1])
            elif args[0] == 'exit':
                break
            elif args[0] == 'help':
                self.help()
            elif args[0] == 'fullwrite':
                self.full_write(args[1])
            elif args[0] == 'fullread':
                self.full_read()
            else:
                print("INVALID COMMAND")


if __name__ == "__main__":
    shell = Shell()

    shell.run()
