import logging
import os
import shutil
import sys

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from api.clients.api_client import ApiClient
from mysql.mysql_client import MysqlClient
from utils.builder import Builder
from fixtures import *


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='http://127.0.0.1:8080/')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


def pytest_configure(config):
    mysql_client = MysqlClient(user="test_qa", password='qa_test', db_name="vkeducation")
    base_dir = base_temp_dir()

    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
        # mysql_client.create_admin()
    mysql_client.connect(db_created=True)

    if not hasattr(config, 'workerinput'):
        mysql_client.create_test_users_table()
        mysql_client.prepare_test_users()
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

    config.mysql_client = mysql_client
    config.base_temp_dir = base_dir


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = 'http://127.0.0.1:4444'
    else:
        selenoid = None
        vnc = False

    return {
        'browser': browser,
        'url': url,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc,
    }


@pytest.fixture()
def api_config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope="function")
def api_client(api_config):
    return ApiClient(api_config['url'])


@pytest.fixture(scope="session", autouse=True)
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope="session")
def admin(mysql_client):
    admin = Builder.user()
    mysql_client.add_user_db(admin)
    return admin


@pytest.fixture(scope="function")
def authorized_api(api_client, admin):
    return api_client.post_login(admin.username, admin.password)
