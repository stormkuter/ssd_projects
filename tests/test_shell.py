from unittest import TestCase
from unittest.mock import patch

from src.shell.shell import Shell
from src.shell.shell_command import WriteCommand

TEST_LBA = 3
TEST_VAL = 0xAAAABBBB


class TestShell(TestCase):
    def setUp(self):
        self.sut = Shell()

    @patch.object(WriteCommand, 'execute', return_value=0)
    def test_write_success(self, mock_write):
        self.assertEqual(0, self.sut.write(TEST_LBA, TEST_VAL))

    @patch.object(WriteCommand, 'execute', return_value=1)
    def test_write_failure(self, mock_write):
        self.assertEqual(1, self.sut.write(TEST_LBA, TEST_VAL))
