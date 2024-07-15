from unittest import TestCase
from unittest.mock import Mock

from src.ssd.hil import HostInterfaceLayer, OpCode

TEST_READ_COMMAND_INPUT = "R"
TEST_WRITE_COMMAND_INPUT = "W"
TEST_WRONG_COMMAND_INPUT = "KKK"
TEST_ADDRESS = 1
TEST_WRONG_ADDRESS = 103
TEST_VALUE = "0x12345678"
TEST_WRONG_VALUE = "0xFFFFFFFFF"

class TestHostInterfaceLayer(TestCase):
    def setUp(self):
        self.sut_hil = HostInterfaceLayer()
        self.fil = Mock()
        self.sut_hil.set_fil(self.fil)

    def test_get_op_code_by_should_return_proper_value_when_arg_is_valid(self):
        # arrange
        expected_result_read = OpCode.READ
        expected_result_write = OpCode.WRITE

        # act & assert
        self.assertEqual(expected_result_read, OpCode.get_op_code_by(TEST_READ_COMMAND_INPUT))
        self.assertEqual(expected_result_write, OpCode.get_op_code_by(TEST_WRITE_COMMAND_INPUT))

    def test_get_op_code_by_should_raise_value_error_when_arg_is_invalid(self):
        # act & assert
        with self.assertRaises(ValueError) as ve:
            OpCode.get_op_code_by(TEST_WRONG_COMMAND_INPUT)
        print(str(ve.exception))

    def test_get_command_should_call_fil_method(self):
        # act
        self.sut_hil.get_command(TEST_READ_COMMAND_INPUT, TEST_ADDRESS)
        self.sut_hil.get_command(TEST_WRITE_COMMAND_INPUT, TEST_ADDRESS, TEST_VALUE)

        # assert
        self.fil.read_lba.assert_called_once()
        self.fil.write_lba.assert_called_once()

    def test_get_command_raise_exception_when_arg_is_invalid(self):
        # act & assert
        with self.assertRaises(ValueError) as ve:
            self.sut_hil.get_command(TEST_READ_COMMAND_INPUT, TEST_WRONG_ADDRESS)
        print(str(ve.exception))

        with self.assertRaises(ValueError) as ve:
            self.sut_hil.get_command(TEST_WRITE_COMMAND_INPUT, TEST_ADDRESS, TEST_WRONG_VALUE)
        print(str(ve.exception))