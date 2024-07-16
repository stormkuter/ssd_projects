from unittest import TestCase
from unittest.mock import Mock

from src.ssd.hil import HostInterfaceLayer, OpCode
from src.ssd.ssd import Ssd


TEST_COMMANDS = ['ssd.py', 'w', '1', '0xFFFFFFFF']

class TestSSD(TestCase):
    def setUp(self):
        self.mock_hil: HostInterfaceLayer = Mock()
        self.sut_ssd = Ssd()
        self.sut_ssd.set_hil(self.mock_hil)

    def test_run_should_call_hil_get_command_when_get_valid_command(self):
        # act
        self.sut_ssd.set_commands(TEST_COMMANDS)
        self.sut_ssd.run()

        # assert
        self.mock_hil.get_command.assert_called_once()

    def test_set_commands_should_return_set_proper_value(self):
        # arrange
        expected_result = OpCode.WRITE

        # act
        self.sut_ssd.set_commands(TEST_COMMANDS)

        # assert
        self.assertEqual(expected_result, self.sut_ssd.get_op_code())
        self.assertEqual(int(TEST_COMMANDS[2]), self.sut_ssd.get_address())
        self.assertEqual(TEST_COMMANDS[3], self.sut_ssd.get_value())

    def test_run_should_raise_exception_without_set_commands(self):
        # act & assert
        with self.assertRaises(AttributeError) as ae:
            ssd = Ssd()
            ssd.run()
        print(str(ae.exception))
