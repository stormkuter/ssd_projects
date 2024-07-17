from src.common.logger import LOGGER
from src.shell.shell_command import create_shell_command, ReturnObject
from src.common import ssd_config


class TestApp:
    def main(self) -> ReturnObject:
        is_mismatched = False
        expected = "0x12345678"
        deprecated = "0xAAAABBBB"
        write_cmd = create_shell_command('write')
        read_cmd = create_shell_command('read')

        for i in range(30):
            for lba in range(0, 6):
                write_cmd.execute(lba, deprecated)

        for lba in range(0, 6):
            write_cmd.execute(lba, expected)

        for lba in range(0, 6):
            read_value = read_cmd.execute(lba).val
            if read_value != expected:
                LOGGER.info(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            LOGGER.info("Data is written well")
            return ReturnObject(0, read_value)
        else:
            return ReturnObject(8, read_value)


def main():
    app = TestApp()
    return app.main()
