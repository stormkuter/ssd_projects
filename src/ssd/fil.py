import os
import enum

INIT_VALUE = '0x00000000'
MAX_ADDRESS = 100


class FilePath(enum.Enum):
    if os.environ.get('ENV', 'prod') == 'test':
        folder_path = os.path.join(os.path.dirname(__file__), '../../tests/data')
    else:
        folder_path = os.path.join(os.path.dirname(__file__), 'data')
    nand_file_path = os.path.join(folder_path, './nand.txt')
    result_file_path = os.path.join(folder_path, './result.txt')

    @classmethod
    def get_folder_path(cls):
        return FilePath.folder_path

    @classmethod
    def get_nand_file_path(cls):
        return FilePath.nand_file_path

    @classmethod
    def get_result_file_path(cls):
        return FilePath.result_file_path


class FlashInterfaceLayer:
    def __init__(self):
        self.__flash_map = {}
        self.__lazy_update = False

        self.folder_path = FilePath.get_folder_path().value
        self.nand_file_path = FilePath.get_nand_file_path().value
        self.result_file_path = FilePath.get_result_file_path().value

        # .data/nand.txt, result.txt 에 유효한 정보가 있다면 읽어서 가져옴
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if not os.path.exists(self.nand_file_path):
            with open(self.nand_file_path, "w") as f:
                for i in range(MAX_ADDRESS - 1):
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
        if not self.__lazy_update:
            pass

    def read_lba(self, lba):
        if not self.__lazy_update:
            # update result.txt
            with open(self.result_file_path, "w") as f:
                f.write(self.__flash_map[lba])
            pass
        return self.__flash_map[lba]

    def flush(self):
        # update nand.txt, result.txt
        pass

    def enable_lasy_update(self):
        self.__lazy_update = False

    def disable_lasy_update(self):
        self.__lazy_update = True
