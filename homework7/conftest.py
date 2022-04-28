import logging
import os

import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError

from client.socket_client import SocketClient
from mock import flask_mock
from application import app
import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 15:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 15s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        log_file = os.path.join(repo_root, 'tmp', 'app.log')
        logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
        env = copy(os.environ)
        env.update({
            'APP_HOST': settings.APP_HOST,
            'APP_PORT': settings.APP_PORT,
            'MOCK_HOST': settings.MOCK_HOST,
            'MOCK_PORT': settings.MOCK_PORT
        })

        app.run_app()
        wait_ready(settings.APP_HOST, settings.APP_PORT)
        flask_mock.run_mock()
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure():
    requests.get(f'http://{settings.APP_HOST}:{settings.APP_PORT}/shutdown_app')
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown_mock')


@pytest.fixture(scope='session')
def api_client():
    return SocketClient()
