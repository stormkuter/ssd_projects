import unittest
import pathlib as pl
import shutil
import os
from unittest import skip

os.environ['ENV'] = 'test'
from src.ssd.fil import FlashInterfaceLayer, FilePath

INIT_VALUE = '0x00000000'
MAX_ADDRESS = 100


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'data'), ignore_errors=True)

        self.sut = FlashInterfaceLayer()
        self.folder_path = FilePath.get_folder_path().value
        self.nand_file_path = FilePath.get_nand_file_path().value
        self.result_file_path = FilePath.get_result_file_path().value

    def test_folder_create(self):
        self.check_folder_exist(self.folder_path)

    def test_nand_file_create_init(self):
        path = pl.Path(self.nand_file_path)

        self.check_file_exist(self.nand_file_path)

        read_data = pl.Path(path).read_text().split('\n')
        self.assertEqual(len(read_data), MAX_ADDRESS)

        for i in range(MAX_ADDRESS):
            if read_data[i] != INIT_VALUE:
                raise AssertionError("initial value is not matched")

    def test_result_file_create_init(self):
        read_data = self.get_file_data(self.result_file_path)

        self.check_file_exist(self.result_file_path)
        self.assertEqual(read_data, INIT_VALUE)

    def test_write_lba_success(self):
        self.sut.enable_lasy_update()
        lba = '0'
        value = '0x10000000'
        self.sut.write_lba(lba, value)

        self.assertEqual(self.sut.read_lba(lba), value)

    def test_read_lba_success(self):
        read_data = self.get_file_data(self.result_file_path)
        lba = 0
        self.assertEqual(self.sut.read_lba(str(lba)), read_data)

    def get_file_data(self, path):
        return pl.Path(path).read_text().split('\n')[0]

    def check_file_exist(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def check_folder_exist(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Folder does not exist: %s" % str(path))


if __name__ == '__main__':
    unittest.main()
