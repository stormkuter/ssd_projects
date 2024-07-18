from src.common.logger import LOGGER
from src.common import ssd_config
from src.shell.script import TestAppBase, ReturnObject


class TestApp(TestAppBase):
    def main(self):
        valid_lbas = [ssd_config.MAX_LBA, str(ssd_config.MIN_LBA), str(ssd_config.MAX_LBA)]
        valid_values = ["0x00000000", hex(ssd_config.MAX_VALUE)]
        invalid_values = [hex(ssd_config.MAX_VALUE + 1)]

        for lba in valid_lbas:
            for value in valid_values:
                ret = self.write(lba, value)
                if ret.err != ssd_config.ERROR_CODE_NONE:
                    LOGGER.debug(f'Error is occurred with "write {lba} {value}" ({ret.err}, {ret.val})')
                    return ReturnObject(-1, None)

        for lba in valid_lbas:
            for value in invalid_values:
                ret = self.write(lba, value)
                if ret.err == ssd_config.ERROR_CODE_NONE:
                    LOGGER.debug(f'Error is expected but not occurred with "write {lba} {value}" ({ret.err}, {ret.val})')
                    return ReturnObject(-1, None)

        return ReturnObject(0, None)


def main():
    app = TestApp()
    return app.main()
