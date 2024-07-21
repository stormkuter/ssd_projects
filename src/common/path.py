import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SOURCE_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOURCE_SSD_DIR = os.path.join(SOURCE_BASE_DIR, "ssd")
SOURCE_SHELL_DIR = os.path.join(SOURCE_BASE_DIR, "shell")
SOURCE_SCRIPT_DIR = os.path.join(SOURCE_SHELL_DIR, "script")

SOURCE_SSD_DATA_DIR = os.path.join(SOURCE_SSD_DIR, "data")
TEST_BASE_DIR = os.path.join(BASE_DIR, "tests/data")

SSD_EXEC = os.path.join(SOURCE_SSD_DIR, "ssd.py")

DATA_FILE_NAND = os.path.join(SOURCE_SSD_DIR, "data/nand.txt")
DATA_FILE_RESULT = os.path.join(SOURCE_SSD_DIR, "data/result.txt")
DATA_FILE_BUFFER = os.path.join(SOURCE_SSD_DIR, "data/buffer.json")

TEST_DATA_FILE_NAND = os.path.join(TEST_BASE_DIR, "nand.txt")
TEST_DATA_FILE_RESULT = os.path.join(TEST_BASE_DIR, "result.txt")
TEST_DATA_FILE_BUFFER = os.path.join(TEST_BASE_DIR, "buffer.json")

LOG_DIR_PATH = os.path.join(SOURCE_BASE_DIR, "common")
LOG_FILE_PATH = os.path.join(LOG_DIR_PATH, "latest.log")
LOG_FILE_SIZE = 1024 * 10

RUNNER_MODE_FILE = os.path.join(SOURCE_BASE_DIR,"RUNNER")