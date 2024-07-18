from src.common import ssd_config
from src.common.path import *

INIT_VALUE = "0x00000000"


class FlashInterfaceLayer:
    def __init__(self, is_test: bool = False):
        self.__flash_map = {}

        if is_test:
            self.folder_path = TEST_BASE_DIR
            self.nand_file_path = TEST_DATA_FILE_NAND
            self.result_file_path = TEST_DATA_FILE_RESULT
        else:
            self.folder_path = SOURCE_SSD_DATA_DIR
            self.nand_file_path = DATA_FILE_NAND
            self.result_file_path = DATA_FILE_RESULT

        self.create_output_files()
        self.update_flash_map()

    def create_output_files(self):
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
        if not os.path.exists(self.nand_file_path):
            with open(self.nand_file_path, "w") as f:
                f.write('\n'.join([INIT_VALUE] * ssd_config.NUM_LBAS))
        if not os.path.exists(self.result_file_path):
            with open(self.result_file_path, "w") as f:
                f.write(f'{INIT_VALUE}')

    def update_flash_map(self):
        with open(self.nand_file_path, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            self.__flash_map[str(i)] = line.strip()

    def write_lba(self, lba, value):
        self.__flash_map[lba] = value
        self.flush()

    def read_lba(self, lba):
        with open(self.result_file_path, "w") as f:
            f.write(self.__flash_map[lba])
        return self.__flash_map[lba]

    def erase_lba(self, lba, size):
        for i in range(int(size)):
            self.__flash_map[str(int(lba) + i)] = INIT_VALUE
        self.flush()

    def flush(self):
        with open(self.nand_file_path, "w") as f:
            for i in range(ssd_config.NUM_LBAS - 1):
                f.write(f"{self.__flash_map[str(i)]}\n")
            f.write(f"{self.__flash_map[str(ssd_config.NUM_LBAS - 1)]}")
