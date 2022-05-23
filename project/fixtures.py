import shutil
import sys

import allure
import pytest
import os

from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.authorized_page import AuthorizedPage


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def authorized_page(driver):
    return AuthorizedPage(driver=driver)


@pytest.fixture
def registration_page(driver, login_page):
    return login_page.go_to_registration_page()


@pytest.fixture
def campaign_page(login):
    return login.go_to_campaign()


@pytest.fixture
def segments_page(login):
    return login.go_to_segments()




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
            'version': '91.0',
            'sessionTimeout': '10m'
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
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()



@pytest.fixture(scope='function')
def auth_page(login_page, admin):
    return login_page.auth(admin.username, admin.password)
