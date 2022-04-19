import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import CampaignPageLocators
import test_data


class CampaignPage(BasePage):
    locators = CampaignPageLocators()

    @allure.step("Create campaign {campaign_name}")
    def create_campaign(self, file_path, campaign_name):
        self.click(CampaignPageLocators.CREATE_CAMPAIGN_LOCATOR)
        self.click(CampaignPageLocators.TRAFFIC_LOCATOR)
        self.send_keys(CampaignPageLocators.LINK_LOCATOR, test_data.LINK_CAMPAIGN)
        self.send_keys(CampaignPageLocators.CAMPAIGN_NAME_LOCATOR, campaign_name)
        self.click(CampaignPageLocators.BANNER_LOCATOR)
        input_field = self.find(CampaignPageLocators.UPLOAD_BANNER_LOCATOR)
        input_field.send_keys(file_path)
        self.click(CampaignPageLocators.SUBMIT_CREATE_LOCATOR)
