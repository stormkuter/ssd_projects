import re
import os, sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

from src.shell.shell_command import create_shell_command
from src.shell.shell_script import ShellOperation


class Shell:

    def __init__(self):
        self.__op = ShellOperation()

    def run(self):
        print('================= SSD Shell Started! =================')

        while True:
            user_inputs = self._get_user_input().split()

            if not self._is_valid_user_input(user_inputs):
                continue

            input_operation = user_inputs[0]

            if input_operation == 'write':
                self.__op.write(user_inputs[1], user_inputs[2])
            elif input_operation == 'read':
                self.__op.read(user_inputs[1])
            elif input_operation == 'exit':
                print('=============== SSD Shell Terminated!  ===============')
                break
            elif input_operation == 'help':
                self.__op.help()
            elif input_operation == 'fullwrite':
                self.__op.full_write(user_inputs[1])
            elif input_operation == 'fullread':
                self.__op.full_read()
            elif input_operation == 'testapp1' or input_operation == 'testapp2':
                import importlib
                import src.shell.script as test_scripts

                modules = test_scripts.list_modules()
                if input_operation in modules:
                    package_name = "src.shell.script"
                    module_name = input_operation

                    full_module_name = f"{package_name}.{module_name}"
                    module = importlib.import_module(full_module_name)

                    if hasattr(module, "main"):
                        func = getattr(module, "main")
                        if callable(func):
                            func()
                        else:
                            print(f"{full_module_name}.main() is not callable.")
                    else:
                        print(f"{full_module_name}.main() is not found.")

    def _get_user_input(self):
        return input(">> ").strip()

    def _is_valid_user_input(self, user_inputs) -> bool:
        args_num_dict = {
            'write': 3,  # write 3 0xAAAABBBB
            'read': 2,  # read 3
            'fullwrite': 2,  # fullwrite 0xAAAABBBB
            'fullread': 1,  # fullread
            'testapp1': 1,  # testapp1
            'testapp2': 1,  # testapp2
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

        if input_operation == 'write' or input_operation == 'read':
            lba = user_inputs[1]
            valid_lba = re.match('^[0-9]{1,2}$', lba)

            if valid_lba is None:
                print("[Warning] Invalid LBA!\nEnter 'help' for details.")
                return False

        if input_operation == 'write':
            val = user_inputs[2]
            valid_val = re.match('^0x[0-9A-Fa-f]{8}$', val)

            if valid_val is None:
                print("[Warning] Invalid Value!\nEnter 'help' for details.")
                return False

        if input_operation == 'fullwrite':
            val = user_inputs[1]
            valid_val = re.match('^0x[0-9A-F]{8}$', val)

            if valid_val is None:
                print("[Warning] Invalid Value!\nEnter 'help' for details.")
                return False

        return True


if __name__ == "__main__":
    shell = Shell()
    shell.run()
