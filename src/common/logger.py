import glob
import inspect
import logging

import os, sys
from datetime import datetime

from concurrent_log_handler import ConcurrentRotatingFileHandler
from src.common.path import LOG_FILE_PATH, LOG_DIR_PATH, LOG_FILE_SIZE

LOGGING_FORMATTER = logging.Formatter('[%(asctime)s] %(func_name)-30s [%(file_name)s : %(func_lino)-4s] : %(message)s',
                                      datefmt='%Y-%m-%d %H:%M')


class CustomRotatingFileHandler(ConcurrentRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = datetime.now().strftime("until_%y%m%d_%Hh_%Mm_%Ss")
        rollover_filename = os.path.join(LOG_DIR_PATH, f"{current_time}.log")

        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, rollover_filename)

        self.mode = 'w'
        self.stream = self._open()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, level, name='CustomLogger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.setup_handler()

    def create_file_handler(self, log_level=logging.DEBUG):
        file_handler = CustomRotatingFileHandler(LOG_FILE_PATH, maxBytes=LOG_FILE_SIZE, backupCount=1024)
        file_handler.setFormatter(LOGGING_FORMATTER)
        file_handler.setLevel(log_level)
        return file_handler

    def create_stream_handler(self, log_level=logging.DEBUG):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(LOGGING_FORMATTER)
        stream_handler.setLevel(log_level)
        return stream_handler

    def setup_handler(self, is_runner=False):
        self.logger.handlers.clear()
        if is_runner:
            stream_handler = self.create_stream_handler(logging.INFO)
        else:
            stream_handler = self.create_stream_handler(logging.DEBUG)

        file_handler = self.create_file_handler(logging.DEBUG)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def _log_with_func_name(self, level, msg):
        self._archive_older_logfiles()

        frame = inspect.currentframe().f_back.f_back
        func_name = frame.f_code.co_name
        func_line_number = frame.f_lineno
        file_name = os.path.basename(frame.f_code.co_filename)
        extra = {'func_name': func_name + "()", 'func_lino': func_line_number, 'file_name': file_name}
        self.logger.log(level, msg, extra=extra)

    def _archive_older_logfiles(self):
        sorted_log_file_list = sorted(glob.glob(LOG_DIR_PATH + "/until_*.log"))
        if len(sorted_log_file_list) > 1:
            sorted_log_file_list.pop(-1)
            for fn in sorted_log_file_list:
                without_extension_filename = os.path.splitext(os.path.basename(fn))[0]
                convert_extension_to_zip = os.path.join(LOG_DIR_PATH, without_extension_filename + ".zip")
                if os.path.exists(convert_extension_to_zip):
                    os.remove(convert_extension_to_zip)
                os.rename(fn, convert_extension_to_zip)

    def debug(self, message):
        self._log_with_func_name(logging.DEBUG, message)

    def info(self, message):
        self._log_with_func_name(logging.INFO, message)

    def warning(self, message):
        self._log_with_func_name(logging.WARNING, message)

    def error(self, message):
        self._log_with_func_name(logging.ERROR, message)

    def critical(self, message):
        self._log_with_func_name(logging.CRITICAL, message)


LOGGER = Logger(logging.DEBUG)
