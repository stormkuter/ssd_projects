import os, sys
import importlib
import time


current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(parent_directory)

import src.shell.script as test_scripts
from src.common import path
from src.common.logger import LOGGER
from src.shell.shell_command import create_shell_command, ReturnObject

class Shell:

    def __init__(self, args):
        self.__args = args
        create_shell_command('flush').execute()

    def __del__(self):
        create_shell_command('flush').execute()

    def run(self):
        if len(self.__args) == 2:
            LOGGER.setup_handler(True)
            run_list_file_path = os.path.join(path.TEST_BASE_DIR, self.__args[1])
            try:
                run_list_file = open(run_list_file_path, "r")
            except Exception:
                print("No Exist Scenario File!")
                return

            while True:
                test_scenario = run_list_file.readline().strip()
                if not test_scenario:
                    break
                # 중복 코드
                modules = test_scripts.list_modules()

                if test_scenario in modules:
                    print(f"{test_scenario} --- Run...", end="")
                    package_name = "src.shell.script"
                    module_name = test_scenario

                    full_module_name = f"{package_name}.{module_name}"
                    module = importlib.import_module(full_module_name)

                    if hasattr(module, "main"):
                        func = getattr(module, "main")
                        if callable(func):
                            ret: ReturnObject = func()
                            if ret.err != 0:
                                print("Fail!")
                                run_list_file.close()
                                return
                            print("Pass")
                        else:
                            LOGGER.debug(f"{full_module_name}.main() is not callable.")
                    else:
                        LOGGER.debug(f"{full_module_name}.main() is not found.")

            run_list_file.close()
            return

        LOGGER.debug('================= SSD Shell Started! =================')

        while True:
            try:
                time.sleep(0.5)
                user_inputs = self._get_user_input().split()
                if not user_inputs: continue

                input_operation = user_inputs[0]

                if input_operation == "exit":
                    LOGGER.debug('=============== SSD Shell Terminated!  ===============')
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
                            LOGGER.debug(f"{full_module_name}.main() is not callable.")
                    else:
                        LOGGER.debug(f"{full_module_name}.main() is not found.")
                else:
                    create_shell_command(input_operation).execute(*user_inputs[1:])

            except Exception as e:
                LOGGER.critical("Shell fail: " + str(e))

    def _get_user_input(self):
        try:
            ret = input(">> ").strip()
        except KeyboardInterrupt as e:
            ret = "exit"

        return ret


if __name__ == "__main__":
    args = sys.argv
    shell = Shell(args)
    shell.run()
