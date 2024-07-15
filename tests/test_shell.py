import io
import sys
from unittest import TestCase
from unittest.mock import patch

from src.shell.shell import Shell
from src.shell.shell_command import WriteCommand, ReadCommand, FullReadCommand, FullWriteCommand

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

    @patch.object(ReadCommand, 'execute', return_value=0)
    def test_read_success(self, mock_read):
        self.assertEqual(0, self.sut.read(TEST_LBA))

    @patch.object(ReadCommand, 'execute', return_value=1)
    def test_read_failure(self, mock_read):
        self.assertEqual(1, self.sut.read(TEST_LBA))

    @patch.object(FullWriteCommand, 'execute', return_value=0)
    def test_full_write_success(self, mock_full_write):
        self.assertEqual(0, self.sut.full_write(TEST_VAL))

    @patch.object(FullWriteCommand, 'execute', return_value=1)
    def test_full_write_failure(self, mock_full_write):
        self.assertEqual(1, self.sut.full_write(TEST_VAL))

    @patch.object(FullReadCommand, 'execute', return_value=0)
    def test_full_read_success(self, mock_full_read):
        self.assertEqual(0, self.sut.full_read())

    @patch.object(FullReadCommand, 'execute', return_value=1)
    def test_full_read_failure(self, mock_full_read):
        self.assertEqual(1, self.sut.full_read())

    @patch.object(Shell, 'help', return_value=1)
    def test_help(self, mock_help):
        self.sut.help()
        self.sut.help.assert_called_once()

    @patch.object(Shell, '_get_user_input', return_value='exit')
    def test_run_exit_success(self, mock_write):
        output = io.StringIO()
        sys.stdout = output

        self.sut.run()

        self.assertTrue('Terminated' in output.getvalue())
        sys.stdout = sys.__stdout__

    @patch.object(Shell, '_get_user_input', side_effect=['', 'exit'])
    def test_run_invalid_command(self, mock_write):
        output = io.StringIO()
        sys.stdout = output

        self.sut.run()

        self.assertTrue('Invalid Command' in output.getvalue())
        sys.stdout = sys.__stdout__

    @patch.object(Shell, '_get_user_input', side_effect=['write 3', 'exit'])
    def test_run_invalid_command_write(self, mock_write):
        output = io.StringIO()
        sys.stdout = output

        self.sut.run()

        self.assertTrue('Invalid Command' in output.getvalue())
        sys.stdout = sys.__stdout__

    @patch.object(Shell, '_get_user_input', side_effect=['read', 'exit'])
    def test_run_invalid_command_read(self, mock_write):
        output = io.StringIO()
        sys.stdout = output

        self.sut.run()

        self.assertTrue('Invalid Command' in output.getvalue())
        sys.stdout = sys.__stdout__

