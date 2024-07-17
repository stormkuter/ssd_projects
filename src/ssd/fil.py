from src.common import ssd_config
from src.common.path import *

INIT_VALUE = '0x00000000'


class FlashInterfaceLayer:
    def __init__(self, is_test: bool = False):
        self.__flash_map = {}
        self.__cache = False

        if is_test:
            self.folder_path = TEST_BASE_DIR
            self.nand_file_path = TEST_DATA_FILE_NAND
            self.result_file_path = TEST_DATA_FILE_RESULT
        else:
            self.folder_path = SOURCE_BASE_DIR
            self.nand_file_path = DATA_FILE_NAND
            self.result_file_path = DATA_FILE_RESULT

        self.create_output_files()

    def create_output_files(self):
        # .data/nand.txt, result.txt 에 유효한 정보가 있다면 읽어서 가져옴
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
        if not os.path.exists(self.nand_file_path):
            with open(self.nand_file_path, "w") as f:
                for i in range(ssd_config.NUM_LBAS - 1):
                    f.write(f'{INIT_VALUE}\n')
                f.write(f'{INIT_VALUE}')
        if not os.path.exists(self.result_file_path):
            with open(self.result_file_path, "w") as f:
                f.write(f'{INIT_VALUE}')
        with open(self.nand_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            self.__flash_map[str(i)] = line.strip()

    def write_lba(self, lba, value):
        self.__flash_map[lba] = value
        if not self.__cache:
            self.flush()

    def read_lba(self, lba):
        if not self.__cache:
            # update result.txt
            with open(self.result_file_path, "w") as f:
                f.write(self.__flash_map[lba])
        return self.__flash_map[lba]

    def erase_lba(self, lba, size):
        for i in range(int(size)):
            self.__flash_map[str(int(lba, 16)+i)] = INIT_VALUE

        if not self.__cache:
            self.flush()

    def flush(self):
        with open(self.nand_file_path, "w") as f:
            for i in range(ssd_config.NUM_LBAS - 1):
                f.write(f'{self.__flash_map[str(i)]}\n')
            f.write(f'{self.__flash_map[str(ssd_config.NUM_LBAS - 1)]}')

    def enable_cache(self):
        self.__cache = False

    def disable_cache(self):
        self.__cache = True

    def get_folder_path(self):
        return self.folder_path

    def get_nand_file_path(self):
        return self.nand_file_path

    def get_result_file_path(self):
        return self.result_file_path
