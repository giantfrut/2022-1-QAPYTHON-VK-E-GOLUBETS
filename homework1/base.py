import pytest
from selenium.webdriver.remote.webelement import WebElement
from ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



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

    def click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def send_keys(self, locator, text, timeout=None) -> WebElement:
        elem = self.find(locator, timeout=timeout)
        elem.click()
        elem.clear()
        elem.send_keys(text)
        elem.send_keys(Keys.RETURN)

    def auth(self):
        email = "giantfrut@gmail.com"
        password = "test13245"
        login_button = self.find(basic_locators.LOGIN_BUTTON)
        login_button.click()
        email_input = self.find(basic_locators.EMAIL_INPUT)
        email_input.send_keys(email)
        password_input = self.find(basic_locators.PASS_INPUT)
        password_input.send_keys(password)
        auth_button = self.find(basic_locators.AUTH_BUTTON)
        auth_button.click()


