import unittest
import pathlib as pl
import os
import shutil
from unittest import skip

os.environ['ENV'] = 'test'
from src.ssd.fil import FlashInterfaceLayer, FilePath

INIT_VALUE = '0x00000000'
TEST_VALUE = '0x12345678'
TEST_ADDRESS = '1'
MAX_ADDRESS = 100


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'data'), ignore_errors=True)

        self.sut = FlashInterfaceLayer()
        self.folder_path = FilePath.get_folder_path()
        self.nand_file_path = FilePath.get_nand_file_path()
        self.result_file_path = FilePath.get_result_file_path()

    def test_folder_create(self):
        self.check_folder_exist(self.folder_path)

    def test_nand_file_create_init(self):
        self.check_file_exist(self.nand_file_path)
        read_data = self.get_file_data(self.nand_file_path)
        self.assertEqual(len(read_data), MAX_ADDRESS)

        for i in range(MAX_ADDRESS):
            if read_data[i] != INIT_VALUE:
                raise AssertionError("initial value is not matched")

    def test_result_file_create_init(self):
        read_data = self.get_file_data(self.result_file_path)

        self.check_file_exist(self.result_file_path)
        self.assertEqual(read_data[0], INIT_VALUE)

    def test_write_lba_success(self):
        self.sut.enable_lasy_update()
        self.sut.write_lba(TEST_ADDRESS, TEST_VALUE)

        self.assertEqual(self.sut.read_lba(TEST_ADDRESS), TEST_VALUE)

    def test_read_lba_success(self):
        read_data = self.get_file_data(self.result_file_path)
        self.assertEqual(self.sut.read_lba(TEST_ADDRESS), read_data[0])

    def get_file_data(self, path):
        return pl.Path(path).read_text().split('\n')

    def check_file_exist(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def check_folder_exist(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Folder does not exist: %s" % str(path))


if __name__ == '__main__':
    unittest.main()
