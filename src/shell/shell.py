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
            user_inputs = self._get_user_input().split()

            if not self._is_valid_user_input(user_inputs):
                continue

            input_operation = user_inputs[0]

            if input_operation == 'write':
                self.write(user_inputs[1], user_inputs[2])
            elif input_operation == 'read':
                self.read(user_inputs[1])
            elif input_operation == 'exit':
                print('=============== SSD Shell Terminated!  ===============')
                break
            elif input_operation == 'help':
                self.help()
            elif input_operation == 'fullwrite':
                self.full_write(user_inputs[1])
            elif input_operation == 'fullread':
                self.full_read()

    def _get_user_input(self):
        return input(">> ").strip()

    def _is_valid_user_input(self, user_inputs) -> bool:
        args_num_dict = {
            'write': 3,  # write 3 0xAAAABBBB
            'read': 2,  # read 3
            'fullwrite': 2,  # fullwrite 0xAAAABBBB
            'fullread': 1,  # fullread
            'exit': 1,  # exit
            'help': 1,  # help
        }

        if not user_inputs:
            print("[Warning] No Operation Input!\nEnter 'help' for details.")
            return False

        input_operation = user_inputs[0]
        if input_operation not in args_num_dict.keys():
            print("[Warning] Invalid Operation!\nEnter 'help' for details.")
            return False

        args_num = len(user_inputs)
        if args_num != args_num_dict[input_operation]:
            print("[Warning] Invalid Operation Format!\nEnter 'help' for details.")
            return False

        return True


if __name__ == "__main__":
    shell = Shell()

    shell.run()
