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

        # if self.authorize:
        #     self.api_client.post_login("giantfrut", "vkeducation")

    # @pytest.fixture(scope='function')
    # def banner_image(self, repo_root):
    #     banner_path = os.path.join(repo_root, 'utils/campaign_banner.jpg')
    #     image = {'file': open(banner_path, 'rb')}
    #     return image
    #
    # @pytest.fixture(scope='function')
    # def campaign(self, banner_image):
    #     resp = self.api_client.post_create_campaign(banner_image)
    #     yield resp['id']
    #     self.api_client.delete_campaign(resp['id'])
    #     assert self.api_client.check_campaign(resp['id'], 'deleted')


