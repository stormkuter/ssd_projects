import unittest
import pathlib as pl
import os
from unittest import skip

from src.ssd.fil import FlashInterfaceLayer

os.environ['ENV'] = 'test'

FOLDER_PATH = os.path.join(os.path.dirname(__file__), 'data')
NAND_FILE_PATH = os.path.join(FOLDER_PATH, './nand.txt')
RESULT_FILE_PATH = os.path.join(FOLDER_PATH, './result.txt')

INIT_VALUE = '0x00000000'
MAX_ADDRESS = 100


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.sut = FlashInterfaceLayer()

    def test_folder_create(self):
        path = pl.Path(FOLDER_PATH)

        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Folder does not exist: %s" % str(path))

    def test_nand_file_create_init(self):
        path = pl.Path(NAND_FILE_PATH)

        if not pl.Path(path).resolve().is_file():
            raise AssertionError("nand.txt File does not exist: %s" % str(path))

        read_data = pl.Path(path).read_text().split('\n')
        self.assertEqual(len(read_data), MAX_ADDRESS)

        for i in range(MAX_ADDRESS):
            if read_data[i] != INIT_VALUE[2:]:
                raise AssertionError("initial value is not matched")

    @skip
    def test_result_file_create_init(self):
        path = pl.Path(RESULT_FILE_PATH)

        if not pl.Path(path).resolve().is_file():
            raise AssertionError("result.txt File does not exist: %s" % str(path))

        read_data = pl.Path(path).read_text().split('\n')
        self.assertEqual(len(read_data), 1)

    @skip
    def test_prev_nand_file_load(self):
        pass

    @skip
    def test_write_lba_success(self):
        pass

    @skip
    def test_write_lba_fail(self):
        pass

    @skip
    def test_read_lba_success(self):
        pass

    @skip
    def test_read_lba_fail(self):
        pass


if __name__ == '__main__':
    unittest.main()
