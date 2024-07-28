import pytest

from commons.BaseClass import BaseClass
from utilities.CustomLogger import Logger


class Test_Login(BaseClass):
    logger = Logger.logger()

    @pytest.mark.smoke
    def test_001_homepage(self):
        pass

    def test_002_homepage(self):
        pass

    def test_003_homepage(self):
        pass
