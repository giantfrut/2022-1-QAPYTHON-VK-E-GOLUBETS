import logging
import os
import shutil
import sys

import pytest

from api.client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture()
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
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

    for handler in log.handlers:
        handler.close()


@pytest.fixture(scope='session')
def credentials(repo_root):
    cred_path = os.path.join(repo_root, 'credentials.txt')
    with open(cred_path, 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    return user, password


@pytest.fixture(scope="function")
def api_client(config, credentials) -> ApiClient:
    api_client = ApiClient(config['url'], *credentials)
    return api_client
