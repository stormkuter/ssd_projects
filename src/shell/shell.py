import os, sys
import importlib
import src.shell.script as test_scripts
from src.common.logger import LOGGER
from src.shell.shell_command import create_shell_command

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)


class Shell:

    def run(self):
        LOGGER.info('================= SSD Shell Started! =================')

        while True:
            try:
                user_inputs = self._get_user_input().split()
                input_operation = user_inputs[0]

                if input_operation == 'exit':
                    LOGGER.info('=============== SSD Shell Terminated!  ===============')
                    break
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
                            LOGGER.info(f"{full_module_name}.main() is not callable.")
                    else:
                        LOGGER.info(f"{full_module_name}.main() is not found.")
                else:
                    create_shell_command(input_operation).execute(*user_inputs[1:])

            except Exception as ex:
                LOGGER.info(ex)
                LOGGER.info("[ERR] Invalid Input!!\nEnter 'help' for details.")

    def _get_user_input(self):
        return input(">> ").strip()


if __name__ == "__main__":
    shell = Shell()
    shell.run()
