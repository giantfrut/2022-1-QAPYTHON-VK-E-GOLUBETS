import allure
import pytest
import test_data
from base import BaseCase


class TestTarget(BaseCase):

    @allure.feature('UI tests')
    @pytest.mark.UI
    def test_invalid_login(self, login_page, invalid_login_page):
        login_page.auth(test_data.NONEXISTENT_EMAIL, test_data.WRONG_PASSWORD)
        assert invalid_login_page.find(invalid_login_page.locators.INVALID_LOGIN_LOCATOR).is_displayed()

    @allure.feature('UI tests')
    @pytest.mark.UI
    def test_incorrect_login(self, login_page):
        login_page.auth(test_data.WRONG_EMAIL, test_data.WRONG_PASSWORD)

        assert login_page.find(login_page.locators.INCORRECT_EMAIL_LOCATOR).is_displayed()

    @allure.feature('UI tests')
    @pytest.mark.UI
    def test_create_campaign(self, file_path, campaign_page):
        campaign_page.create_campaign(file_path, test_data.CAMPAIGN_NAME)

        assert campaign_page.find((campaign_page.locators.CAMPAIGN_LOCATOR[0],
                                   campaign_page.locators.CAMPAIGN_LOCATOR[1].format(name=test_data.CAMPAIGN_NAME)))

    @allure.feature('UI tests')
    @pytest.mark.UI
    def test_create_segment(self, segments_page):
        segments_page.create_segment(test_data.SEGMENT_NAME)
        assert segments_page.find((segments_page.locators.CHOOSE_SEGMENT_LOCATOR[0],
                                   segments_page.locators.CHOOSE_SEGMENT_LOCATOR[1].format(
                                       name=test_data.SEGMENT_NAME)))
        segments_page.delete_segment(test_data.SEGMENT_NAME)

    @allure.feature('UI tests')
    @pytest.mark.UI
    def test_delete_segment(self, segments_page):
        segments_page.create_segment(test_data.SEGMENT_NAME)
        segments_page.delete_segment(test_data.SEGMENT_NAME)
        assert segments_page.check_invisibility((segments_page.locators.CHOOSE_SEGMENT_LOCATOR[0],
                                                 segments_page.locators.CHOOSE_SEGMENT_LOCATOR[1].format(
                                                     name=test_data.SEGMENT_NAME)))
