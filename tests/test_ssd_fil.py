import unittest
import pathlib as pl
import os

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



if __name__ == '__main__':
    unittest.main()
