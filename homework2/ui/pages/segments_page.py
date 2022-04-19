import allure

from ui.pages.base_page import BasePage
from ui.locators.locators import SegmentsPageLocators


class SegmentsPage(BasePage):
    locators = SegmentsPageLocators()

    @allure.step("Create segment {segment_name}")
    def create_segment(self, segment_name):
        if self.find(SegmentsPageLocators.NEW_SEGMENT_LOCATOR).is_displayed():
            self.click(SegmentsPageLocators.NEW_SEGMENT_LOCATOR)
        else:
            self.click(SegmentsPageLocators.CREATE_SEGMENT_LOCATOR)
        self.click(SegmentsPageLocators.APPS_SEGMENT_LOCATOR)
        self.click(SegmentsPageLocators.SEGMENT_CHECKBOX_LOCATOR)
        self.click(SegmentsPageLocators.ADD_SEGMENT_LOCATOR)
        self.send_keys(SegmentsPageLocators.SEGMENT_NAME_LOCATOR, segment_name)
        self.click(SegmentsPageLocators.CONFIRM_CREATE_SEGMENT_LOCATOR)

    @allure.step("Delete segment {segment_name}")
    def delete_segment(self, segment_name):
        self.find((SegmentsPageLocators.CHOOSE_SEGMENT_LOCATOR[0],
                   SegmentsPageLocators.CHOOSE_SEGMENT_LOCATOR[1].format(name=segment_name)))
        self.click((SegmentsPageLocators.DELETE_SEGMENT_LOCATOR[0],
                    SegmentsPageLocators.DELETE_SEGMENT_LOCATOR[1].format(name=segment_name)))
        self.click(SegmentsPageLocators.SUBMIT_DELETE_LOCATOR)
        self.check_invisibility(SegmentsPageLocators.PROCESS_DELETE_LOCATOR)
