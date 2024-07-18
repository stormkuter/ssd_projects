import random

from src.common.logger import LOGGER
from src.common import ssd_config
from src.shell.script import TestAppBase, ReturnObject


class TestApp(TestAppBase):
    def main(self):
        init_value = self.get_random_value()
        self.full_write(init_value)
        self.flush()

        lba_range = self.get_random_lba_range()
        expected = {}
        for lba in range(lba_range[0], lba_range[1] + 1):
            expected[lba] = init_value

        for i in range(5 * ssd_config.COMMAND_BUFFER_SIZE):
            opc = random.randrange(0, 3)
            lba = self.get_random_lba(lba_range[0], lba_range[1])
            value = self.get_random_value()

            if opc == 0:
                ret = self.read(lba)
                LOGGER.debug(f"[Command {i + 1}] read({lba})")
                if ret.err:
                    LOGGER.debug(f'Error is occurred with "read {lba}" ({ret.err}, {ret.val})')
                    return ReturnObject(-1, None)
                else:
                    if ret.val != expected[lba]:
                        LOGGER.debug(f'Data mismatch with "read {lba}" (expected: {expected[lba]}, real: {ret.val})')
                        return ReturnObject(-1, None)
            elif opc == 1:
                ret = self.write(lba, value)
                LOGGER.debug(f"[Command {i + 1}] write({lba}, {value})")
                if ret.err:
                    LOGGER.debug(f'Error is occurred with "write {lba} {value}" ({ret.err}, {ret.val})')
                    return ReturnObject(-1, None)
                else:
                    expected[lba] = value

            elif opc == 2:
                ret = self.erase(lba, 1)
                LOGGER.debug(f"[Command {i + 1}] erase({lba}, {1})")
                if ret.err:
                    LOGGER.debug(f'Error is occurred with "erase {lba} 1" ({ret.err}, {ret.val})')
                    return ReturnObject(-1, None)
                else:
                    expected[lba] = ssd_config.ERASED_VALUE

        return ReturnObject(0, None)


def main():
    app = TestApp()
    return app.main()
