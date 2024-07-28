import time
from typing import Tuple
from selenium.common import NoSuchElementException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec


class BasePage:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    def _open_url(self, page_url: str):
        self._driver.get(page_url)

    # get browser information
    def _get_page_title(self) -> str:
        return self._driver.title

    def _get_page_url(self) -> str:
        return self._driver.current_url

    # navigation
    def _back_to_page(self):
        self._driver.back()

    def _forward_to_page(self):
        self._driver.forward()

    def _refresh_current_page(self):
        self._driver.refresh()

    # alert
    def _wait_for_alert_present(self, time: int = 10) -> Alert:
        explicit_wait = WebDriverWait(self._driver, time)
        return explicit_wait.until(ec.alert_is_present())

    def _accept_alert(self, time: int = 10):
        alert = self._wait_for_alert_present(time)
        alert.accept()

    def _cancel_alert(self, time: int = 10):
        alert = self._wait_for_alert_present(time)
        alert.dismiss()

    def _get_text_alert(self, time: int = 10) -> str:
        alert = self._wait_for_alert_present(time)
        return alert.text

    def _sendkeys_to_alert(self, text_value: str, time: int = 10):
        alert = self._wait_for_alert_present(time)
        alert.send_keys(text_value)

    # windows and tabs
    def _switch_to_window_by_id(self, expected_window_id: str):
        for window_handle in self._driver.window_handles:
            if window_handle != expected_window_id:
                self._driver.switch_to.window(window_handle)
                break

    def _switch_to_window_by_title(self, expected_page_title: str):
        for window_handle in self._driver.window_handles:
            self._driver.switch_to.window(window_handle)
            if window_handle.title().casefold() == expected_page_title.casefold():
                break

    def _close_all_windows_without_parent(self, parent_window_id: str):
        for window_handle in self._driver.window_handles:
            if window_handle != parent_window_id:
                self._driver.switch_to.window(window_handle)
                self._driver.close()
            self._driver.switch_to.window(parent_window_id)

    def _open_new_window(self):
        self._driver.switch_to.new_window('window')

    def _create_new_tab(self):
        self._driver.switch_to.new_window('tab')

    # element locators
    def _get_dynamic_xpath(self, locator_type: str, *dynamic_value: str) -> str:
        locator_type = locator_type.format(*dynamic_value)
        return locator_type

    def _get_locator(self, locator: str, *dynamic_value: str) -> tuple:
        __locator = ()
        if locator.lower().startswith("id="):
            __locator = (By.ID, locator[3:])
        elif locator.lower().startswith("name="):
            __locator = (By.ID, locator[5:])
        elif locator.lower().startswith("class="):
            __locator = (By.ID, locator[6:])
        elif locator.lower().startswith("css="):
            __locator = (By.ID, locator[4:])
        elif locator.lower().startswith("xpath="):
            if "{" in locator:
                __locator = (By.XPATH, _get_dynamic_xpath(locator, *dynamic_value)[6:])
            else:
                __locator = (By.XPATH, locator[6:])
        else:
            RuntimeError
        return __locator

    def _get_web_element(self, locator: str, *dynamic_value: str) -> WebElement:
        return self._driver.find_element(self._get_locator(locator, dynamic_value)[0], self._get_locator(locator, dynamic_value)[1])

    def _get_list_web_elements(self, locator: str, *dynamic_value: str) -> list[WebElement]:
        return self._driver.find_elements(self._get_locator(locator, dynamic_value)[0], self._get_locator(locator, dynamic_value)[1])

    def _click_to_element(self, locator: str, *dynamic_value: str):
        self._wait_for_element_clickable(locator, 10, dynamic_value)
        self._get_web_element(locator, dynamic_value).click()

    def _sendkeys_to_element(self, locator: str, text_value: str, *dynamic_value: str):
        self._wait_for_element_visible(locator, 10, dynamic_value)
        self._get_web_element(locator, dynamic_value).clear()
        self._get_web_element(locator, dynamic_value).send_keys(text_value)

    def _get_element_text(self, locator: str, *dynamic_value: str) -> str:
        return self._get_web_element(locator, dynamic_value).text

    def _get_element_attribute(self, locator: str, attribute_name: str, *dynamic_value: str) -> str:
        return self._get_web_element(locator, dynamic_value).get_attribute(attribute_name)

    def _get_element_css(self, locator: str, property_name: str, *dynamic_value: str) -> str:
        return self._get_web_element(locator, dynamic_value).value_of_css_property(property_name)

    def _get_element_size(self, locator: str, *dynamic_value: str) -> int:
        list_web_elements = self._get_list_web_elements(locator, dynamic_value)
        return len(list_web_elements)

    def _is_element_displayed(self, locator: str, *dynamic_value: str) -> bool:
        try:
            return self._get_web_element(locator, dynamic_value).is_displayed()
        except NoSuchElementException:
            return False

    def _is_element_undisplayed(self, locator: str, *dynamic_value: str) -> bool:
        self._override_implicit_wait(5)
        list_web_elements = self._get_list_web_elements(locator, dynamic_value)
        self._override_implicit_wait(10)
        return True if len(list_web_elements) == 0 or (len(list_web_elements) > 0 and not(list_web_elements[0].is_displayed())) else False

    def _is_element_enable(self, locator: str, *dynamic_value: str) -> bool:
        return self._get_web_element(locator, dynamic_value).is_enabled()

    def _is_element_selected(self, locator: str, *dynamic_value: str) -> bool:
        return self._get_web_element(locator, dynamic_value).is_selected()

    # dropdown
    def _select_item_in_default_dropdown(self, locator: str, text_item: str, *dynamic_value: str):
        select = Select(self._get_web_element(locator, dynamic_value))
        select.select_by_visible_text(text_item)

    def _get_selected_option_in_default_dropdown(self, locator: str, *dynamic_value: str) -> str:
        select = Select(self._get_web_element(locator, dynamic_value))
        return select.first_selected_option

    def _is_dropdown_multiple(self, locator: str, *dynamic_value: str) -> bool:
        select = Select(self._get_web_element(locator, dynamic_value))
        return select.is_multiple

    def _select_item_in_custom_dropdown(self, parent_locator: str, child_locator: str, text_item: str, *dynamic_value: str):
        self._get_web_element(parent_locator, dynamic_value).click()
        time.sleep(1)
        explicit_wait = WebDriverWait(self._driver, 10)
        explicit_wait.until(ec.visibility_of_all_elements_located(self._get_locator(child_locator, dynamic_value)))
        list_items = self._get_list_web_elements(child_locator, dynamic_value)
        for item in list_items:
            if item.text.strip() == text_item:
                self._scroll_to_element(child_locator, dynamic_value)
                time.sleep(1)
                item.click()

    # checkbox/radio button
    def _check_to_default_checkbox_radiobutton(self, locator: str, *dynamic_value: str):
        element = self._get_web_element(locator, dynamic_value)
        if not(element.is_selected()):
            element.click()

    def _uncheck_to_default_checkbox(self, locator: str, *dynamic_value: str):
        element = self._get_web_element(locator, dynamic_value)
        if element.is_selected():
            element.click()

    # frame/iframe
    def _switch_to_frame_iframe(self, locator: str, *dynamic_value: str):
        self._driver.switch_to.frame(self._get_web_element(locator, dynamic_value))

    def _switch_to_default_content(self):
        self._driver.switch_to.default_content()

    # mouse action
    def _hover_to_element(self, locator: str, *dynamic_value: str):
        ActionChains(driver) \
            .move_to_element(self._get_web_element(locator, dynamic_value)) \
            .perform()

    def _double_click_to_element(self, locator: str, *dynamic_value: str):
        ActionChains(driver) \
            .double_click(self._get_web_element(locator, dynamic_value)) \
            .perform()

    def _right_click_to_element(self, locator: str, *dynamic_value: str):
        ActionChains(driver) \
            .context_click(self._get_web_element(locator, dynamic_value)) \
            .perform()

    # keyboard action
    def _press_key_to_element(self, locator: str, key: Keys, *dynamic_value: str):
        ActionChains(driver) \
            .send_keys_to_element(self._get_web_element(locator, dynamic_value), key) \
            .perform()

    # javascript executor
    def _scroll_to_bottom_page(self):
        self._driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    def _highlight_element(self, locator: str, *dynamic_value: str):
        original_style = self._get_element_attribute(locator, "style", dynamic_value)
        self._driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, "style",
                                    "border: 2px solid red; border-style: dashed;");
        time.sleep(1)
        self._driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, "style",
                                    original_style);

    def _click_to_element_by_js(self, locator: str, *dynamic_value: str):
        self._driver.execute_script("arguments[0].click();", self._get_web_element(locator, dynamic_value));

    def _scroll_to_element(self, locator: str, *dynamic_value: str):
        self._driver.execute_script("arguments[0].scrollIntoView(true);", self._get_web_element(locator, dynamic_value));

    def _get_element_validation_message(self, locator: str, *dynamic_value: str) -> str:
        return str(self._driver.execute_script("return arguments[0].validationMessage;"), self._get_web_element(locator, dynamic_value))

    def _is_image_loaded(self, locator: str, *dynamic_value: str) -> bool:
        return bool(self._driver.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != \"undefined\" && arguments[0].naturalWidth > 0", self._get_web_element(locator, dynamic_value)))

    def _is_page_loadded_success(self) -> bool:
        page_state = self._driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    # wait
    def _wait_for_element_visible(self, locator: str, time: int, *dynamic_value: str):
        explicit_wait = WebDriverWait(self._driver, time)
        explicit_wait.until(ec.visibility_of_element_located(self._get_locator(locator, dynamic_value)))

    def _wait_for_all_elements_visible(self, locator: str, time: int, *dynamic_value: str):
        explicit_wait = WebDriverWait(self._driver, time)
        explicit_wait.until(ec.visibility_of_all_elements_located(self._get_locator(locator, dynamic_value)))

    def _wait_for_element_invisible(self, locator: str, time: int, *dynamic_value: str):
        explicit_wait = WebDriverWait(self._driver, time)
        explicit_wait.until(ec.invisibility_of_element_located(self._get_locator(locator, dynamic_value)))

    def _wait_for_element_clickable(self, locator: str, time: int, *dynamic_value: str):
        explicit_wait = WebDriverWait(self._driver, time)
        explicit_wait.until(ec.element_to_be_clickable(self._get_locator(locator, dynamic_value)))

    def _override_implicit_wait(self, time: int):
        self._driver.implicitly_wait(time)
