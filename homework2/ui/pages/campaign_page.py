import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import CampaignPageLocators
import test_data


class CampaignPage(BasePage):
    locators = CampaignPageLocators()

    @allure.step("Create campaign")
    def create_campaign(self, file_path):
        self.click(CampaignPageLocators.CREATE_CAMPAIGN_LOCATOR)
        self.click(CampaignPageLocators.TRAFFIC_LOCATOR)
        self.send_keys(CampaignPageLocators.LINK_LOCATOR, test_data.LINK_CAMPAIGN)
        campaign_name = self.find(CampaignPageLocators.CAMPAIGN_NAME_LOCATOR).get_attribute("value")
        self.click(CampaignPageLocators.BANNER_LOCATOR)
        input_field = self.find(CampaignPageLocators.UPLOAD_BANNER_LOCATOR)
        input_field.send_keys(file_path)
        # self.wait(CampaignPageLocators.UPLOAD_PROCESS_LOCATOR)
        self.click(CampaignPageLocators.SUBMIT_CREATE_LOCATOR)

        return campaign_name
