import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import LoginPageLocators


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step("Auth to website with email {email} and password {password}")
    def auth(self, email, password):
        self.click(LoginPageLocators.LOGIN_LOCATOR)
        self.send_keys(LoginPageLocators.EMAIL_LOCATOR, email)
        self.send_keys(LoginPageLocators.PASSWORD_LOCATOR, password)
        self.click(LoginPageLocators.AUTH_LOCATOR)
