from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from commons.BasePage import BasePage


class LoginPage(BasePage):
    __username_textbox = "xpath=//input[@name='username']"
    __password_textbox = "xpath=//input[@name='password']"
    __login_button = "xpath=//button[contains(@class, 'orangehrm-login-button')]"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def input_to_username_textbox(self, username: str):
        super()._sendkeys_to_element(self.__username_textbox, username)

    def input_to_password_textbox(self, password: str):
        super()._sendkeys_to_element(self.__password_textbox, password)

    def click_on_login_button(self):
        super()._click_to_element(self.__login_button)
