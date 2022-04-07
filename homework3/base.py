import os
import pytest


class BaseApi:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.post_login()

    @pytest.fixture(scope='function')
    def banner_image(self, repo_root):
        banner_path = os.path.join(repo_root, 'utils/campaign_banner.jpg')
        image = {'file': open(banner_path, 'rb')}
        return image

    @pytest.fixture(scope='function')
    def campaign(self, banner_image):
        resp = self.api_client.post_create_campaign(banner_image)
        yield resp['id']
        self.api_client.post_delete_campaign(resp['id'])
        assert self.api_client.check_campaign(resp['id'], 'deleted')
