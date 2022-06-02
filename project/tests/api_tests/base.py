import pytest

from mysql.mysql_client import MysqlClient


class MysqlBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup_mysql(self, mysql_client, logger):
        self.mysql_client: MysqlClient = mysql_client
        self.logger = logger
        self.prepare()


class BaseApi(MysqlBase):
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup_api(self, api_client, logger):
        self.api_client = api_client
        self.logger = logger
