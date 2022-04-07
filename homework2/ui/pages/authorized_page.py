import allure

from ui.pages.base_page import BasePage
from ui.pages.segments_page import SegmentsPage
from ui.pages.campaign_page import CampaignPage
from ui.locators.locators import AuthorizedPageLocators


class AuthorizedPage(BasePage):
    locators = AuthorizedPageLocators()

    @allure.step("Go to the campaign page")
    def go_to_campaign(self):
        self.click(AuthorizedPageLocators.DASHBOARD_LOCATOR)
        return CampaignPage(self.driver)

    @allure.step("Go to the segments page")
    def go_to_segments(self):
        self.click(AuthorizedPageLocators.SEGMENTS_LOCATOR)
        return SegmentsPage(self.driver)
