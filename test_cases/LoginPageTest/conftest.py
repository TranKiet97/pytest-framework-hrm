import pytest
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
from utilities.ReadProperties import ReadConfig
from pathlib import Path


__url = ReadConfig.get_application_url()


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


# @pytest.fixture(scope="class", params=["chrome", "firefox"])
@pytest.fixture(scope="class")
def setup(request):
    # run with custom command
    browser_name = request.config.getoption("browser_name")

    # run with list of browser
    # browser_name = request.param

    if browser_name == "firefox":
        # handling notification popups
        ops = webdriver.FirefoxOptions().add_argument("--disable-notifications")
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=ops)
    elif browser_name == "chrome":
        # handling notification popups
        ops = webdriver.ChromeOptions().add_argument("--disable-notifications")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ops)
    driver.get(__url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield
    driver.quit()


# hook for adding environment info to HTML report
def pytest_configure(config):
    config.metadata['Project Name'] = 'OrangeHRM'
    config.metadata['Module Name'] = 'Regression Testing'
    config.metadata['Tester'] = 'Kane Tran'


# hook for delete/modify environment info to HTML report
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)


# specifying report folder location and save report with timestamp
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = str(Path(__file__).resolve().parents[2]) + "\\reports\\HTML_reports\\" + "report-" + datetime.now().strftime(
        "%d-%m-%Y %H-%M-%S") + ".html"
