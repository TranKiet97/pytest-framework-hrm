import pytest

from commons.BaseClass import BaseClass
from page_objects.LoginPage import LoginPage
from utilities.CustomLogger import Logger
from utilities.ReadProperties import ReadConfig


class Test_Login(BaseClass):
    logger = Logger.logger()

    def test_001_login_successful(self):
        self.logger.info("*** TC 001: Verify user can login to page successful ***")
        self.logger.info("Step 01: Navigate to Login page")
        login_page = LoginPage(self.driver)

        self.logger.info("Step 02: Input username into Username textbox")
        login_page.input_to_username_textbox(ReadConfig.get_user_name())

        self.logger.info("Step 03: Input password into Password textbox")
        login_page.input_to_password_textbox(ReadConfig.get_password())

        self.logger.info("Step 04: Click on Login button")
        login_page.click_on_login_button()

    def test_002_hard_assert(self):
        self.logger.info("*** TC 002: Verify hard asserts work correctly ***")
        self.hard_assert_equal('1', '1')
        self.hard_assert_is('test', 'test')
        self.hard_assert_in('do', 'to do')
        self.hard_assert_contains([1, 2, 3], 1)

    def test_003_soft_assert(self):
        self.logger.info("*** TC 003: Verify soft asserts work correctly ***")
        self.soft_assert_equal('1', '1')
        self.soft_assert_is('test', 'test')
        self.soft_assert_in('do', 'to do')
        self.soft_assert_contains([1, 2, 3], 1)
        self.assert_all()
