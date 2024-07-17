import unittest
import pathlib as pl
import os
import shutil

from src.common import ssd_config
from src.ssd.fil import FlashInterfaceLayer

INIT_VALUE = '0x00000000'
TEST_VALUE = '0x12345678'
TEST_ADDRESS = '1'
TEST_SIZE = '10'


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'data'), ignore_errors=True)

        self.sut = FlashInterfaceLayer(True)
        self.folder_path = self.sut.get_folder_path()
        self.nand_file_path = self.sut.get_nand_file_path()
        self.result_file_path = self.sut.get_result_file_path()

    def test_folder_create(self):
        self.check_folder_exist(self.folder_path)

    def test_nand_file_create_init(self):
        self.check_file_exist(self.nand_file_path)
        read_data = self.get_file_data(self.nand_file_path)
        self.assertEqual(len(read_data), ssd_config.NUM_LBAS)

        for i in range(ssd_config.NUM_LBAS):
            if read_data[i] != INIT_VALUE:
                raise AssertionError("initial value is not matched")

    def test_result_file_create_init(self):
        read_data = self.get_file_data(self.result_file_path)

        self.check_file_exist(self.result_file_path)
        self.assertEqual(read_data[0], INIT_VALUE)

    def test_write_lba_success(self):
        self.sut.enable_cache()
        self.sut.write_lba(TEST_ADDRESS, TEST_VALUE)

        self.assertEqual(self.sut.read_lba(TEST_ADDRESS), TEST_VALUE)

    def test_read_lba_success(self):
        self.assertEqual(self.sut.read_lba(TEST_ADDRESS), self.get_file_data(self.result_file_path)[0])

    def test_erase_lba_success(self):
        self.sut.enable_cache()
        for i in range(int(TEST_SIZE)):
            self.sut.write_lba(str(int(TEST_ADDRESS)+i), str(hex(int(TEST_VALUE, 16)+i)))

        self.sut.erase_lba(TEST_ADDRESS, TEST_SIZE)

        for i in range(int(TEST_SIZE)):
            self.assertEqual(self.sut.read_lba(str(int(TEST_ADDRESS)+i)), INIT_VALUE)

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
