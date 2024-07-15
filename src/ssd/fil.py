class FlashInterfaceLayer:
    def __init__(self):
        # .tmp/nand.txt, result.txt 에 유효한 정보가 있다면 읽어서 가져옴
        self.__flash_map = {}
        self.__lazy_update = False
        pass

    def write_lba(self, lba, value):
        self.__flash_map[lba] = value
        if not self.__lazy_update:
            # update nand.txt
            pass

    def read_lba(self, lba):
        if not self.__lazy_update:
            # update result.txt
            pass
        return self.__flash_map[lba]

    def flush(self):
        # update nand.txt, result.txt
        pass
