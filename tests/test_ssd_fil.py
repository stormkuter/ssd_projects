import unittest
import pathlib as pl
import os
from unittest import skip

os.environ['ENV'] = 'test'
from src.ssd.fil import FlashInterfaceLayer, FilePath

INIT_VALUE = '0x00000000'
MAX_ADDRESS = 100


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.sut = FlashInterfaceLayer()
        self.folder_path = FilePath.get_folder_path().value
        self.nand_file_path = FilePath.get_nand_file_path().value
        self.result_file_path = FilePath.get_result_file_path().value

    def test_folder_create(self):
        path = pl.Path(self.folder_path)

        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Folder does not exist: %s" % str(path))

    def test_nand_file_create_init(self):
        path = pl.Path(self.nand_file_path)

        if not pl.Path(path).resolve().is_file():
            raise AssertionError("nand.txt File does not exist: %s" % str(path))

        read_data = pl.Path(path).read_text().split('\n')
        self.assertEqual(len(read_data), MAX_ADDRESS)

        for i in range(MAX_ADDRESS):
            if read_data[i] != INIT_VALUE[2:]:
                raise AssertionError("initial value is not matched")

    @skip
    def test_result_file_create_init(self):
        path = pl.Path(self.result_file_path)

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
