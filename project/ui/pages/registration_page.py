import allure

from ui.pages.authorized_page import AuthorizedPage
from ui.pages.base_page import BasePage
from ui.locators.locators import RegistrationPageLocators


class ValidationError(Exception):
    pass


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()
    REG_URL = "http://127.0.0.1:8080/reg"

    @allure.step("Registration new {user}")
    def registration(self, user, confirm_password, accept=True):
        self.send_keys(RegistrationPageLocators.NAME_LOCATOR, user.username)
        self.send_keys(RegistrationPageLocators.SURNAME_LOCATOR, user.surname)
        self.send_keys(RegistrationPageLocators.MIDDLE_NAME_LOCATOR, user.middle_name)
        self.send_keys(RegistrationPageLocators.USERNAME_LOCATOR, user.username)
        self.send_keys(RegistrationPageLocators.EMAIL_LOCATOR, user.email)
        self.send_keys(RegistrationPageLocators.PASSWORD_LOCATOR, user.password)
        self.send_keys(RegistrationPageLocators.REPEAT_PASSWORD_LOCATOR, confirm_password)
        if accept:
            self.click(RegistrationPageLocators.ACCEPT_LOCATOR)
        self.click(RegistrationPageLocators.REGISTER_BUTTON)
        return AuthorizedPage(self.driver)

    @allure.step("Check registration fields validation")
    def reg_check_validation(self):
        fields = [self.locators.NAME_LOCATOR, self.locators.SURNAME_LOCATOR, self.locators.USERNAME_LOCATOR,
                  self.locators.EMAIL_LOCATOR, self.locators.PASSWORD_LOCATOR, self.locators.REPEAT_PASSWORD_LOCATOR,
                  self.locators.ACCEPT_LOCATOR]

        for locator in fields:
            if self.check_validation(locator) is None:
                return False
        return True

    @allure.step("Go to the login page")
    def go_to_login_page(self):
        self.click(self.locators.LOGIN_LINK)
