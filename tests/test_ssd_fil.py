import unittest
import pathlib as pl

from src.ssd.fil import FlashInterfaceLayer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.sut = FlashInterfaceLayer()

    def test_folder_exist(self):
        path = pl.Path('../src/ssd/data/')

        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Folder does not exist: %s" % str(path))


if __name__ == '__main__':
    unittest.main()
