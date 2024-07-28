import configparser
import os.path
from pathlib import Path

file_path = str(Path(__file__).resolve().parents[1]) + '\\configurations\\config.ini'
config = configparser.RawConfigParser()
config.read(file_path)


class ReadConfig:
    @staticmethod
    def get_application_url() -> str:
        return config.get('common_info', 'base_url')

    @staticmethod
    def get_user_name() -> str:
        return config.get('common_info', 'user_name')

    @staticmethod
    def get_password() -> str:
        return config.get('common_info', 'password')
