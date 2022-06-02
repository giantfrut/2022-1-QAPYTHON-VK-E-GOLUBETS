import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import LoginPageLocators
from ui.pages.registration_page import RegistrationPage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    @allure.step("Auth with username and password: {username} , {password} ")
    def auth(self, username, password):
        self.send_keys(LoginPageLocators.USERNAME_LOCATOR, username)
        self.send_keys(LoginPageLocators.PASSWORD_LOCATOR, password)
        self.click(LoginPageLocators.AUTH_LOCATOR)

    @allure.step("Go to the registration page")
    def go_to_registration_page(self):
        self.click(LoginPageLocators.REGISTRATION_LINK)
        return RegistrationPage(self.driver)
