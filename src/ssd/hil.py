# import enum
#
# from src.common.path import DATA_FILE_RESULT
# from src.ssd.command_buffer import CommandBuffer
# from src.ssd.fil import FlashInterfaceLayer
# from src.ssd.op_code import OpCode
#
# MIN_VALUE = 0
# MAX_VALUE = 2 ** 32 - 1
# MIN_ADDRESS = 0
# MAX_ADDRESS = 99
#
#
# class HostInterfaceLayer:
#
#     def __init__(self, command_buffer: CommandBuffer):
#         self.__fil = None
#         self.command_buffer = command_buffer
#
#     def set_fil(self, fil: FlashInterfaceLayer):
#         self.__fil = fil
#
#
#     # TODO :: 이 친구도 리팩토링 대상 1
#     def execute(self, *args):
#         self.__validation_args(args)
#         op_code = OpCode.get_op_code_by(args[0])
#         if op_code == OpCode.READ:
#             try:
#                 buffered_data = self.command_buffer.execute(args)
#                 with open(DATA_FILE_RESULT, "w") as f:
#                     f.write(buffered_data)
#             except ValueError as ve:
#                 self.__fil.read_lba(args[1])
#         elif op_code == OpCode.FLUSH:
#             self.command_buffer.flush()
#             command_list = self.command_buffer.get_commands_requiring_save()
#             for command in command_list:
#                 op_code = OpCode.get_op_code_by(command[0])
#                 self.get_command(op_code, command[1:])
#         else:       # Wrtie / Erase
#             if self.command_buffer.is_full_commands():
#                 self.command_buffer.flush()
#                 command_list = self.command_buffer.get_commands_requiring_save()
#                 for command in command_list:
#                     op_code = OpCode.get_op_code_by(command[0])
#                     self.get_command(op_code, command[1:])
#             self.command_buffer.execute(args)
#
#
#     # TODO :: 이 친구도 리팩토링 대상 2
#     def get_command(self, op_code: OpCode, *args, **kwargs):
#         args = args[0]
#         if op_code == OpCode.READ:
#             self.__fil.read_lba(args[0])
#         elif op_code == OpCode.WRITE:
#             value = self.to_upper(args[1])
#             self.__fil.write_lba(args[0], value)
#
#     def to_upper(self, value: str):
#         return value[:2] + value[2:].upper()
#
#     def __validation_args(self, args):
#         if len(args) == 0:
#             raise ValueError("입력 주소 및 값이 없습니다.")
#         if len(args) > 1:
#             self.__validation_of_address(args[1])
#         if len(args) == 3:
#             self.__validation_of_value(args[2])
#
#     def __validation_of_address(self, address):
#         if not isinstance(address, str) or (MIN_ADDRESS > int(address)) or (int(address) > MAX_ADDRESS):
#             raise ValueError(f"입력된 주소값이 잘못 되었습니다.: {address}")
#
#     def __validation_of_value(self, value: str):
#         if len(value) != 10 or value[:2] != "0x":
#             if value.isdigit() and 1 <= int(value) <= 10:
#                 return
#             else:
#                 raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.: {value}")
#         result_value = 0
#         for i in range(2, 10):
#             result_value += self.__to_int(value[i]) * 16 ** (9-i)
#         if (MIN_VALUE > result_value) or (result_value > MAX_VALUE):
#             raise ValueError(f"입력된 값이 잘못 되었습니다.: {value}")
#
#     def __to_int(self, spell: str):
#         spell_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
#         if spell.isdigit():
#             return int(spell)
#         elif spell.upper() in spell_dict:
#             return spell_dict[spell.upper()]
#         else:
#             raise ValueError(f"입력된 값의 형식이 잘못 되었습니다.")
