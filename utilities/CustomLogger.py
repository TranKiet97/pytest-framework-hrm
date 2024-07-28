import logging
import os
from pathlib import Path


class Logger:
    @staticmethod
    def logger():
        path = str(Path(__file__).resolve().parents[1]) + '\\logs\\test_result.log'
        logging.basicConfig(filename=path, format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', force=True,
                            filemode="w")  # filemode='w' to clear all old data in file log before run test cases
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger
