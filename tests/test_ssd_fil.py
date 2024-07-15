import unittest
import pathlib as pl
import os
from unittest import skip

from src.ssd.fil import FlashInterfaceLayer

FOLDER_PATH = '../src/ssd/data'
NAND_FILE_PATH = os.path.join(FOLDER_PATH, './nand.txt')


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

        self.assertEqual(len(pl.Path(path).read_text().split('\n')), 100)

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
