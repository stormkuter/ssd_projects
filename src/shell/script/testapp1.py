from src.shell.shell_command import create_shell_command, ReturnObject
from src.common import ssd_config


class TestApp:
    def main(self):
        is_mismatched = False
        expected = "0x12345678"

        fullwrite_cmd = create_shell_command('fullwrite')
        fullwrite_cmd.execute(expected)

        read_cmd = create_shell_command('read')
        for lba in range(ssd_config.NUM_LBAS):
            read_value = read_cmd.execute(lba).val
            if read_value != expected:
                print(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            print("Data is written well")
            return ReturnObject(0, read_value)
        else:
            return ReturnObject(7, read_value)


def main():
    app = TestApp()
    app.main()
