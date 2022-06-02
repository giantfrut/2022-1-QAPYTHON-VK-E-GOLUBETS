import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import AuthorizedPageLocators


class AuthorizedPage(BasePage):
    locators = AuthorizedPageLocators()

