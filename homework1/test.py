import pytest
from base import BaseCase
from ui.locators import basic_locators
import time



class TestOne(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.auth()
        username_wrap = self.find(basic_locators.USERNAME_WRAP).is_displayed()

        assert username_wrap == True

    @pytest.mark.UI
    def test_logout(self):
        self.auth()
        self.click(basic_locators.USERNAME_WRAP)
        self.find(basic_locators.LOGOUT_BUTTON, timeout=10)
        time.sleep(5)
        self.click(basic_locators.LOGOUT_BUTTON)
        assert self.driver.current_url == "https://target.my.com/"

    @pytest.mark.UI
    def test_edit_contacts(self):
        self.auth()
        self.click(basic_locators.PROFILE_BUTTON)
        self.send_keys(basic_locators.NAME_INPUT, "Ivanov Ivan Ivanovich")
        self.click(basic_locators.PHONE_INPUT)
        self.send_keys(basic_locators.PHONE_INPUT, "79216566981")
        self.click(basic_locators.SAVE_PROFILE_BUTTON)

        assert self.find(basic_locators.NAME_INPUT).get_attribute("value") == "Ivanov Ivan Ivanovich"
        assert self.find(basic_locators.PHONE_INPUT).get_attribute("value") == "79216566981"

    testdata = [
        (basic_locators.STATISTICS_BUTTON, 'https://target.my.com/statistics/summary'),
        (basic_locators.TOOLS_BUTTON, 'https://target.my.com/tools/feeds')
    ]

    @pytest.mark.UI
    @pytest.mark.parametrize('menu_button, expected_result', testdata)
    def test_menu(self, menu_button, expected_result):
        self.auth()
        self.click(menu_button)
        self.page_url(expected_result, timeout=10)
        assert self.driver.current_url == expected_result
