from src.common.logger import LOGGER
from src.common import ssd_config
from src.shell.script import TestAppBase, ReturnObject


class TestApp(TestAppBase):
    def main(self):
        valid_lbas = [ssd_config.MIN_LBA, ssd_config.MAX_LBA, str(ssd_config.MIN_LBA), str(ssd_config.MAX_LBA)]
        invalid_lbas = [ssd_config.MIN_LBA - 1, ssd_config.MAX_LBA + 1, str(ssd_config.MIN_LBA - 1),
                        str(ssd_config.MAX_LBA + 1)]

        valid_lba_ranges = [(ssd_config.MIN_LBA, ssd_config.MAX_LBA),
                            (str(ssd_config.MIN_LBA), str(ssd_config.MAX_LBA)),
                            (str(ssd_config.MIN_LBA), ssd_config.MAX_LBA),
                            (ssd_config.MIN_LBA, str(ssd_config.MAX_LBA))]

        invalid_lba_ranges = [(ssd_config.MIN_LBA - 1, ssd_config.MAX_LBA + 2),
                            (str(ssd_config.MIN_LBA - 1), str(ssd_config.MAX_LBA + 2)),
                            (str(ssd_config.MIN_LBA - 1), ssd_config.MAX_LBA + 2),
                            (ssd_config.MIN_LBA - 1, str(ssd_config.MAX_LBA + 2))]

        for lba in valid_lbas:
            ret = self.read(lba)
            if ret.err != ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is occurred with "read {lba}" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

            ret = self.write(lba, "0x12345678")
            if ret.err != ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is occurred with "write {lba} value" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

            ret = self.erase(lba, 1)
            if ret.err != ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is occurred with "erase {lba} 1" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

        for lba in invalid_lbas:
            ret = self.read(lba)
            if ret.err == ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is expected but not occurred with "read {lba}" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

            ret = self.write(lba, "0x12345678")
            if ret.err == ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is expected but not occurred with "write {lba} value" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

            ret = self.erase(lba, 1)
            if ret.err == ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is expected but not occurred with "erase {lba} 1" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

        for lba_range in valid_lba_ranges:
            ret = self.erase_range(lba_range[0], lba_range[1])
            if ret.err != ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is occurred with "erase_range {lba_range}" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

        for lba_range in invalid_lba_ranges:
            ret = self.erase_range(lba_range[0], lba_range[1])
            if ret.err == ssd_config.ERROR_CODE_NONE:
                LOGGER.debug(f'Error is expected but not occurred with "erase_range {lba_range}" ({ret.err}, {ret.val})')
                return ReturnObject(-1, None)

        return ReturnObject(0, None)


def main():
    app = TestApp()
    return app.main()
