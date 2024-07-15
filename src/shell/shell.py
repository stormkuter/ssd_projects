from src.shell.shell_command import create_shell_command


class Shell:

    def __init__(self):
        self.__command = None

    def write(self, lba, val) -> int:
        self.__command = create_shell_command('write', lba, val)
        return_code = self.__command.execute()

        if not return_code == 0:
            pass

        return return_code

    def read(self, lba):
        self.__command = create_shell_command('read', lba)
        return_code = self.__command.execute()

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
        self.__command = create_shell_command('fullwrite', val)
        return_code = self.__command.execute()

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
            user_input = self._get_user_input()
            args = user_input.split()

            if not self.is_valid_user_input(args):
                continue

            if args[0] == 'write':
                self.write(args[1], args[2])
            elif args[0] == 'read':
                self.read(args[1])
            elif args[0] == 'exit':
                print('=============== SSD Shell Terminated!  ===============')
                break
            elif args[0] == 'help':
                self.help()
            elif args[0] == 'fullwrite':
                self.full_write(args[1])
            elif args[0] == 'fullread':
                self.full_read()

    def _get_user_input(self):
        return input(">> ").strip()

    def is_valid_user_input(self, args) -> bool:
        args_num_dict = {
            'write': 3,
            'read': 2,
            'exit': 1,
            'help': 1,
            'fullwrite': 2,
            'fullread': 1,
        }

        args_num = len(args)

        if args_num < 1:
            print("[Warning] Invalid Command!\nEnter help for details.")
            return False

        input_command = args[0]

        if input_command not in args_num_dict.keys():
            print("[Warning] Invalid Command!\nEnter help for details.")
            return False

        if args_num != args_num_dict[input_command]:
            print("[Warning] Invalid Command!\nEnter help for details.")
            return False

        return True


if __name__ == "__main__":
    shell = Shell()

    shell.run()
