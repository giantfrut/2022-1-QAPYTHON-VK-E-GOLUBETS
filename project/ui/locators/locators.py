from selenium.webdriver.common.by import By


class BasePageLocators:
    ERROR_MESSAGE = (By.XPATH, "//div[@id='flash']")


class LoginPageLocators(BasePageLocators):
    USERNAME_LOCATOR = (By.NAME, "username")
    PASSWORD_LOCATOR = (By.NAME, "password")
    AUTH_LOCATOR = (By.CSS_SELECTOR, "input[value='Login']")
    REGISTRATION_LINK = (By.XPATH, "//a[@href='/reg']")


class RegistrationPageLocators(BasePageLocators):
    NAME_LOCATOR = (By.ID, "user_name")
    SURNAME_LOCATOR = (By.ID, "user_surname")
    MIDDLE_NAME_LOCATOR = (By.ID, "user_middle_name")
    USERNAME_LOCATOR = (By.ID, "username")
    EMAIL_LOCATOR = (By.ID, "email")
    PASSWORD_LOCATOR = (By.ID, "password")
    REPEAT_PASSWORD_LOCATOR = (By.ID, "confirm")
    ACCEPT_LOCATOR = (By.XPATH, "//input[@id = 'term']")
    REGISTER_BUTTON = (By.ID, "submit")
    ERROR_FLASH = (By.XPATH, "//div[contains(@class, 'uk-alert')]")
    LOGIN_LINK = (By.XPATH, "//a[@href = '/login']")


class AuthorizedPageLocators(BasePageLocators):

    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/logout']")
    VK_ID_LOCATOR = (By.XPATH, "//div[@id ='login-name']//li[3]")
    API_BUTTON = (By.XPATH, "//a[@href = 'https://en.wikipedia.org/wiki/Application_programming_interface']")
    INTERNET_BUTTON = (By.XPATH, "//a[@href = 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/']")
    SMTP_BUTTON = (By.XPATH, "//a[@href = 'https://ru.wikipedia.org/wiki/SMTP']")
    PYTHON_FACT = (By.XPATH, "//div[contains(@class, 'uk-text-center')]/p")
    BRAND_BUTTON = (By.XPATH, "//a[contains(@class, 'uk-navbar-brand')]")
    HOME_BUTTON = (By.XPATH, "//li/a[@href='/']")
    PYTHON_BUTTON = (By.XPATH, "//a[@href='https://www.python.org/']")
    PYTHON_HISTORY_BUTTON = (By.XPATH, "//a[@href='https://en.wikipedia.org/wiki/History_of_Python']")
    FLASK_BUTTON = (By.XPATH, "//a[@href='https://flask.palletsprojects.com/en/1.1.x/#']")
    LINUX_BUTTON = (By.XPATH, "//a[@href='javascript:' and text()='Linux']")
    CENTOS_BUTTON = (By.XPATH, "//a[@href='https://www.centos.org/download/']")
    NETWORK_BUTTON = (By.XPATH, "//a[@href='javascript:' and text()='Network']")
    WIRESHARK_NEWS = (By.XPATH, "//a[@href='https://www.wireshark.org/news/']")
    WIRESHARK_DOWNLOAD = (By.XPATH, "//a[@href='https://www.wireshark.org/#download']")
    TCPDUMP_EXAMPLE = (By.XPATH, "//a[@href='https://hackertarget.com/tcpdump-examples/']")
