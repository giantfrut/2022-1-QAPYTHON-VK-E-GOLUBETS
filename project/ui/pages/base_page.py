import time

import allure
import logging

from ui.locators.locators import BasePageLocators
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 5


class BasePage(object):
    locators = BasePageLocators()
    BASE_URL = "http://127.0.0.1:8080/"

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('test')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Click on {locator}")
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                self.find(locator, timeout=timeout)
                self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                if i == CLICK_RETRY - 1:
                    raise

    @allure.step("Send {text} to {locator}")
    def send_keys(self, locator, text, timeout=None):
        elem = self.find(locator, timeout=timeout)
        self.click(locator)
        elem.clear()
        elem.send_keys(text)

    @allure.step("Check fields validation of {locator}")
    def check_validation(self, locator):
        return self.find(locator).get_attribute('required')

    def find_text(self, locator):
        return self.wait(5).until(EC.visibility_of_element_located(locator)).text

    @allure.step("Switch to text window")
    def switch_to_next_window(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("Hover on {locator}")
    def hover_on_element(self, locator):
        element = self.find(locator)
        ActionChains(self.driver).move_to_element(element).perform()
