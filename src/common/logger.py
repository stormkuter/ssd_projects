import glob
import inspect
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from src.common.path import LOG_FILE_PATH, LOG_DIR_PATH


class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # Determine the rollover filename format
        current_time = datetime.now().strftime("until_%y%m%d_%Hh_%Mm_%Ss")
        rollover_filename = os.path.join(LOG_DIR_PATH, f"{current_time}.log")

        # Rename the current log file to the rollover filename
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, rollover_filename)

        # Reopen the log file in write mode
        self.mode = 'w'
        self.stream = self._open()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self, name='CustomLogger', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.formatter = logging.Formatter('[%(asctime)s] %(func_name)-40s [line: %(func_lino)s]] : %(message)s',
                                           datefmt='%Y-%m-%d %H:%M')
        self.logger.setLevel(level)
        self._setup_handler()

    def create_file_handler(self):
        file_handler = CustomRotatingFileHandler(LOG_FILE_PATH, maxBytes=10240, backupCount=1024)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(logging.INFO)
        return file_handler

    def create_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        stream_handler.setLevel(logging.INFO)
        return stream_handler

    def _setup_handler(self):
        self.logger.handlers.clear()
        stream_handler = self.create_stream_handler()
        file_handler = self.create_file_handler()
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def set_stream_handler_silence(self):
        self.logger.handlers.clear()
        file_handler = self.create_file_handler()
        self.logger.addHandler(file_handler)

    def _log_with_func_name(self, level, msg):
        self._archive_older_logfiles()

        frame = inspect.currentframe().f_back.f_back
        module_func_name = frame.f_code.co_qualname
        func_line_number = frame.f_code.co_firstlineno
        extra = {'func_name': module_func_name, 'func_lino': func_line_number}
        self.logger.log(level, msg, extra=extra)

    def _archive_older_logfiles(self):
        sorted_log_file_list = sorted(glob.glob(LOG_DIR_PATH + "/until_*.log"))
        if len(sorted_log_file_list) > 2:
            sorted_log_file_list.pop(0)
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


LOGGER = Logger()
