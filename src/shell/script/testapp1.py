from src.common.logger import LOGGER
from src.common import ssd_config
from src.shell.script import TestAppBase, ReturnObject


class TestApp(TestAppBase):
    def main(self):
        is_mismatched = False
        expected = "0x12345678"

        self.full_write(expected)

        for lba in range(ssd_config.NUM_LBAS):
            read_value = self.read(lba).val
            if read_value != expected:
                LOGGER.debug(f"[WARN] Data mismatch (expected: {expected}, real: {read_value})")
                is_mismatched = True

        if not is_mismatched:
            LOGGER.debug("Data is written well")
            return ReturnObject(0, None)
        else:
            return ReturnObject(-1, None)


def main():
    app = TestApp()
    return app.main()
