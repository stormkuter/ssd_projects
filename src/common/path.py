import os

SOURCE_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOURCE_SSD_DIR = os.path.join(SOURCE_BASE_DIR, "ssd")
SOURCE_SHELL_DIR = os.path.join(SOURCE_BASE_DIR, "shell")

DATA_FILE_NAND = os.path.join(SOURCE_SSD_DIR, "data/nand.txt")
DATA_FILE_RESULT = os.path.join(SOURCE_SSD_DIR, "data/result.txt")