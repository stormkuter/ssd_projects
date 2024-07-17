from src.shell.shell_script import ShellOperation
from src.common import ssd_config


class TestApp(ShellOperation):
    def main(self):
        is_mismatched = False
        expected = "0x12345678"
        deprecated = "0xAAAABBBB"

        for i in range(30):
            for lba in range(0, 6):
                self.write(lba, deprecated)

        for lba in range(0, 6):
            self.write(lba, expected)

        for lba in range(0, 6):
            read_value = self.read(lba).val
            if read_value != expected:
                print(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            print("Data is written well")


def main():
    app = TestApp()
    app.main()
