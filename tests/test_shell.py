import io
import sys
from unittest import TestCase
from unittest.mock import patch

from src.shell.shell import Shell
from src.shell.shell_script import ShellOperation
from src.shell.shell_command import WriteCommand, ReadCommand, FullReadCommand, FullWriteCommand

TEST_LBA = '3'
TEST_VAL = '0xAAAABBBB'

INVALID_LBA_MINUS = '-1'
INVALID_LBA_PLUS = '100'
INVALID_VAL_WITHOUT_0x = 'AAAABBBB'
INVALID_VAL_NOT_TEN_CHAR = '0xAAAABBBBBB'


class TestShell(TestCase):
    def setUp(self):
        self.__op = ShellOperation()
        self.sut = Shell()

        self.output = io.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch.object(WriteCommand, 'execute', return_value=(0, None))
    def test_write_success(self, mock_write):
        self.assertEqual(0, self.__op.write(TEST_LBA, TEST_VAL).err)

    @patch.object(WriteCommand, 'execute', return_value=(1, None))
    def test_write_failure(self, mock_write):
        self.assertEqual(1, self.__op.write(TEST_LBA, TEST_VAL).err)

    @patch.object(ReadCommand, 'execute', return_value=(0, None))
    def test_read_success(self, mock_read):
        self.assertEqual(0, self.__op.read(TEST_LBA).err)

    @patch.object(ReadCommand, 'execute', return_value=(1, None))
    def test_read_failure(self, mock_read):
        self.assertEqual(1, self.__op.read(TEST_LBA).err)

    @patch.object(FullWriteCommand, 'execute', return_value=(0, None))
    def test_full_write_success(self, mock_full_write):
        self.assertEqual(0, self.__op.full_write(TEST_VAL).err)

    @patch.object(FullWriteCommand, 'execute', return_value=(1, None))
    def test_full_write_failure(self, mock_full_write):
        self.assertEqual(1, self.__op.full_write(TEST_VAL).err)

    @patch.object(FullReadCommand, 'execute', return_value=(0, None))
    def test_full_read_success(self, mock_full_read):
        self.assertEqual(0, self.__op.full_read().err)

    @patch.object(FullReadCommand, 'execute', return_value=(1, None))
    def test_full_read_failure(self, mock_full_read):
        self.assertEqual(1, self.__op.full_read().err)

    @patch.object(ShellOperation, 'help', return_value=(1, None))
    def test_help(self, mock_help):
        self.__op.help()
        self.__op.help.assert_called_once()

    @patch.object(Shell, '_get_user_input', return_value='exit')
    def test_run_exit_success(self, mock_write):
        self.sut.run()

        self.assertTrue('Terminated' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=['', 'exit'])
    def test_run_invalid_operation(self, mock_write):
        self.sut.run()

        self.assertTrue('No Operation Input' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=['write 3', 'exit'])
    def test_run_invalid_operation_write(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Operation Format' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=['read', 'exit'])
    def test_run_invalid_operation_read(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Operation Format' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=['fullwrite', 'exit'])
    def test_run_invalid_operation_fullwrite(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Operation Format' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=['fullread 3', 'exit'])
    def test_run_invalid_operation_fullread(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Operation Format' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=[f'wrote {TEST_LBA} {TEST_VAL}', 'exit'])
    def test_run_invalid_operation_typo(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Operation' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=[f'write {INVALID_LBA_MINUS} {TEST_VAL}', 'exit'])
    def test_run_invalid_lba_minus(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid LBA' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=[f'write {INVALID_LBA_PLUS} {TEST_VAL}', 'exit'])
    def test_run_invalid_lba_plus(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid LBA' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=[f'write {TEST_LBA} {INVALID_VAL_WITHOUT_0x}', 'exit'])
    def test_run_invalid_value_without_0x(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Value' in self.output.getvalue())

    @patch.object(Shell, '_get_user_input', side_effect=[f'write {TEST_LBA} {INVALID_VAL_NOT_TEN_CHAR}', 'exit'])
    def test_run_invalid_value_not_ten_char(self, mock_write):
        self.sut.run()

        self.assertTrue('Invalid Value' in self.output.getvalue())
