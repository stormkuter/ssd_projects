from unittest import TestCase
from unittest.mock import Mock

from src.ssd.hil import HostInterfaceLayer, OpCode

TEST_READ_COMMAND_INPUT = "R"
TEST_WRITE_COMMAND_INPUT = "W"
TEST_WRONG_COMMAND_INPUT = "KKK"

class TestHostInterfaceLayer(TestCase):
    def setUp(self):
        self.sut_hil = HostInterfaceLayer()
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
            print(ve)

    def test_get_command(self):
        self.fail()
