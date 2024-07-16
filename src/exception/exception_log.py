import datetime
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)


class ExceptionLog:
    @classmethod
    def get_log_msg(cls, ex: Exception, msg: str):
        now_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        header = f"[ {now_time} ] "
        return header + msg + ": " + str(ex)