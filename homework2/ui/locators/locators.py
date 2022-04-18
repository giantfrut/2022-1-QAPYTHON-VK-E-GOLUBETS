from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_LOCATOR = (By.CSS_SELECTOR, "div[class^='responseHead-module-button']")


class LoginPageLocators(BasePageLocators):
    EMAIL_LOCATOR = (By.NAME, "email")
    PASSWORD_LOCATOR = (By.NAME, "password")
    AUTH_LOCATOR = (By.CSS_SELECTOR, "div[class^='authForm-module-button']")
    INCORRECT_EMAIL_LOCATOR = (
        By.XPATH, "//div[contains(@class, 'authForm-module-notify')]/div[contains(@class, 'undefined')]")


class InvalidLoginLocators(BasePageLocators):
    INVALID_LOGIN_LOCATOR = (By.XPATH, "//div[contains(@class, 'formMsg_title')]")


class AuthorizedPageLocators(BasePageLocators):
    DASHBOARD_LOCATOR = (By.CSS_SELECTOR, "a[href='/dashboard']")
    SEGMENTS_LOCATOR = (By.CSS_SELECTOR, "a[href='/segments']")


class CampaignPageLocators(AuthorizedPageLocators):
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, "//div[contains(@class, 'dashboard-module-createButtonWrap')]/div")
    TRAFFIC_LOCATOR = (By.CSS_SELECTOR, "div[class$='traffic']")
    LINK_LOCATOR = (By.CSS_SELECTOR, "input[data-gtm-id='ad_url_text']")
    CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]/div[@class='input__wrap']/input")
    BANNER_LOCATOR = (By.CSS_SELECTOR, "div[id^='patterns_banner']")
    UPLOAD_BANNER_LOCATOR = (
        By.XPATH, "//div[contains(@class, 'upload-module-wrapper')]/input[contains(@data-test, 'image_240x400')]")
    UPLOAD_PROCESS_LOCATOR = (By.XPATH, "//div[contains(@class, 'roles-module-uploadButton')]")
    SUBMIT_CREATE_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-save-button-wrap')]/button")
    CAMPAIGN_LOCATOR = (By.XPATH, "//a[@title='{name}']")


class SegmentsPageLocators(AuthorizedPageLocators):
    NEW_SEGMENT_LOCATOR = (By.CSS_SELECTOR, "a[href='/segments/segments_list/new/']")
    CREATE_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-create-button-wrap')]/button")
    APPS_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'adding-segments-item')][8]")
    SEGMENT_CHECKBOX_LOCATOR = (By.XPATH, "//input[contains(@class, 'adding-segments-source__checkbox')]")
    ADD_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-add-button')]/button")
    SEGMENT_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]/div/input")
    CONFIRM_CREATE_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-create-segment-button-wrap')]/button")
    CHOOSE_SEGMENT_LOCATOR = (By.XPATH, "//a[@title='{name}']")
    DELETE_SEGMENT_LOCATOR = (By.XPATH, "//a[@title='{name}']/ancestor::div/following-sibling::div[4]/span")
    SUBMIT_DELETE_LOCATOR = (By.XPATH, "//button[contains(@class, 'button_confirm-remove')]")
    PROCESS_DELETE_LOCATOR = (By.XPATH,
                              "//button[contains(@class, 'button_confirm-remove button_general button_pending')]")
