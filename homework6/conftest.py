import os

import pytest
from mysql.client import MysqlClient
import pandas as pd


def pytest_configure(config):
    mysql_client = MysqlClient(user="root", password='0000', db_name="TEST_SQL")
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_total_requests_table()
        mysql_client.create_count_types_table()
        mysql_client.create_user_errors_table()
        mysql_client.create_frequent_requests_table()
        mysql_client.create_server_errors_table()

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def logfile(repo_root):
    return os.path.join(repo_root, "access.log")


@pytest.fixture(scope='session')
def dataframe(logfile):
    df = pd.read_csv(logfile,
                     sep=' ',
                     usecols=[0, 5, 6, 7],
                     names=['ip_addr', 'request', 'status', 'bytes'],
                     na_values='-',
                     header=None,
                     low_memory=False
                     )

    df = df.fillna(0)
    df['bytes'] = df['bytes'].astype('int')
    new_df = df['request'].str.split(' ', expand=True)
    new_df.columns = ['method', 'request', 'protocol']

    df = df.drop(df.columns[[1]], axis=1)
    final_df = pd.concat([df, new_df], axis=1)
    yield final_df
