from selenium.webdriver.common.by import By

LOGIN_BUTTON = (By.XPATH, '//div[text()="Войти" or text()="Log in"]')
EMAIL_INPUT = (By.NAME, 'email')
PASS_INPUT = (By.NAME, 'password')
AUTH_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')
USERNAME_WRAP = (By.XPATH, '//div[contains(@class, "right-module-userNameWrap")]')
LOGOUT_BUTTON = (By.CSS_SELECTOR, 'a[href="/logout"]')
NAME_INPUT = (By.XPATH, '//div[@data-name="fio"]//input')
PHONE_INPUT = (By.XPATH, '//div[@data-name="phone"]//input')
SAVE_PROFILE_BUTTON = (By.XPATH, '//div[contains(@class, "button__text")]')

PROFILE_BUTTON = (By.XPATH, '//a[@href="/profile"]')
TOOLS_BUTTON = (By.XPATH, '//a[@href="/tools"]')
STATISTICS_BUTTON = (By.XPATH, '//a[@href="/statistics"]')
