import os

FOLDER_PATH = os.path.join(os.path.dirname(__file__), 'data')
NAND_FILE_PATH = os.path.join(FOLDER_PATH, './nand.txt')


class FlashInterfaceLayer:
    def __init__(self):
        self.__flash_map = {}
        self.__lazy_update = False

        # .data/nand.txt, result.txt 에 유효한 정보가 있다면 읽어서 가져옴
        if not os.path.exists(FOLDER_PATH):
            os.mkdir(FOLDER_PATH)

        if not os.path.exists(NAND_FILE_PATH):
            with open(NAND_FILE_PATH, "w") as f:
                for i in range(99):
                    f.write(f'{"00000000"}\n')
                f.write(f'{"00000000"}')

    def write_lba(self, lba, value):
        self.__flash_map[lba] = value
        if not self.__lazy_update:
            pass

    def read_lba(self, lba):
        if not self.__lazy_update:
            # update result.txt
            pass
        return self.__flash_map[lba]

    def flush(self):
        # update nand.txt, result.txt
        pass
