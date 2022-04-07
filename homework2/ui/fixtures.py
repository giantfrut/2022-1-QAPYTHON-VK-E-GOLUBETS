import shutil
import sys

import allure
import pytest
import os

from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
import test_data

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.invalid_login_page import InvalidLoginPage
from ui.pages.authorized_page import AuthorizedPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def invalid_login_page(driver):
    return InvalidLoginPage(driver=driver)


@pytest.fixture
def authorized_page(driver):
    return AuthorizedPage(driver=driver)


@pytest.fixture
def campaign_page(login):
    return login.go_to_campaign()


@pytest.fixture
def segments_page(login):
    return login.go_to_segments()


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


def get_driver(browser_name):
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '98.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def cookies(config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.auth(test_data.EMAIL, test_data.PASSWORD)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='function')
def file_path(repo_root):
    return os.path.join(repo_root, "files", "campaign_banner.jpg")


@pytest.fixture(scope='function')
def login(driver, request: FixtureRequest, authorized_page):
    with allure.step("Get cookies"):
        cookies = request.getfixturevalue('cookies')
    with allure.step("Add cookies"):
        for cookie in cookies:
            driver.add_cookie(cookie)

    with allure.step("Refresh page"):
        driver.refresh()

    yield authorized_page
