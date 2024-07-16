from src.shell.shell_script import ShellOperation


class Shell:

    def __init__(self):
        self.__op = ShellOperation()

    def run(self):
        print('================= SSD Shell Started! =================')
        while True:
            user_input = self._get_user_input()
            args = user_input.split()

            if not self.is_valid_user_input(args):
                continue

            if args[0] == 'write':
                self.__op.write(args[1], args[2])
            elif args[0] == 'read':
                self.__op.read(args[1])
            elif args[0] == 'exit':
                print('=============== SSD Shell Terminated!  ===============')
                break
            elif args[0] == 'help':
                self.__op.help()
            elif args[0] == 'fullwrite':
                self.__op.full_write(args[1])
            elif args[0] == 'fullread':
                self.__op.full_read()

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
