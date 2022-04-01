import pytest
import constans
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption('--url', default=constans.BASE_URL)


@pytest.fixture()
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture()
def driver(config):
    url = config['url']
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


