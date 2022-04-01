import pytest
import constans
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    TimeoutException
from ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def page_url(self, expected_result=None, timeout=None):
        return self.wait(timeout).until(EC.url_contains(expected_result))

    def click(self, locator, timeout=None):
        for i in range(constans.CLICK_RETRY):
            try:
                self.find(locator, timeout=timeout)
                self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException):
                if i == constans.CLICK_RETRY - 1:
                    raise

    def send_keys(self, locator, text, timeout=None):
        elem = self.find(locator, timeout=timeout)
        elem.click()
        elem.clear()
        elem.send_keys(text)

    def auth(self):
        self.click(basic_locators.LOGIN_BUTTON)
        self.send_keys(basic_locators.EMAIL_INPUT, constans.EMAIL)
        self.send_keys(basic_locators.PASS_INPUT, constans.PASSWORD)
        self.click(basic_locators.AUTH_BUTTON)
