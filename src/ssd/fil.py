import os

FOLDER_PATH = os.path.join(os.path.dirname(__file__), 'data')
NAND_FILE_PATH = os.path.join(FOLDER_PATH, './nand.txt')
INIT_VALUE = 0x00000000


class FlashInterfaceLayer:
    def __init__(self):
        self.__flash_map = {}
        self.__lazy_update = False

        # .data/nand.txt, result.txt 에 유효한 정보가 있다면 읽어서 가져옴
        if not os.path.exists(FOLDER_PATH):
            os.mkdir(FOLDER_PATH)


        pass

    def write_lba(self, lba, value):
        self.__flash_map[lba] = value
        if not self.__lazy_update:
            # update nand.txt
            # with open(filename, "w") as f:
            #     result = f.write(value)
            pass

        # return result

    def read_lba(self, lba):
        if not self.__lazy_update:
            # update result.txt
            pass
        return self.__flash_map[lba]

    def flush(self):
        # update nand.txt, result.txt
        pass
