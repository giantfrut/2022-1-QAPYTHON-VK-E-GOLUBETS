import pytest

from base import BaseApi


class TestApi(BaseApi):
    @pytest.mark.API
    def test_create_segment(self):
        segment_id = self.api_client.post_create_segment()['id']
        assert self.api_client.check_segment_id(segment_id) is True
        self.api_client.delete_segment(segment_id)

    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.api_client.post_create_segment()['id']
        self.api_client.delete_segment(segment_id)
        assert self.api_client.check_segment_id(segment_id) is False

    @pytest.mark.API
    def test_create_campaign(self, campaign):
        assert self.api_client.check_campaign(campaign, 'active')
