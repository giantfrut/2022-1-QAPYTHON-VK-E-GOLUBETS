import pytest

from mysql.client import MysqlClient


class MysqlBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.prepare()
