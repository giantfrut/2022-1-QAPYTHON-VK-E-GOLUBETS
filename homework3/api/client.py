import logging
import faker
import requests

from urllib.parse import urljoin
from utils.json_data import campaign_payload, segment_payload

MAX_RESPONSE_LENGTH = 300
logger = logging.getLogger('test')
fake = faker.Faker()


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password

        self.session = requests.Session()
        self.csrf_token = None

    @property
    def headers(self):
        return {
            "X-CSRFToken": self.csrf_token
        }

    @property
    def auth_headers(self):
        return {
            "Referer": self.base_url
        }

    def _request(self, method, location, headers=None, files=None, data=None, json=None, params=None,
                 expected_status=200,
                 jsonify=True):
        url = urljoin(self.base_url, location)
        headers = headers or self.headers
        response = self.session.request(method, url, headers=headers, files=files, data=data, json=json, params=params)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.request} for URL "{url}"')

        if jsonify:
            return response.json()
        return response

    def get_csrf(self):
        res = self._request("get", "https://target.my.com/csrf/", jsonify=False)
        self.csrf_token = res.cookies.get("csrftoken")

    def post_login(self):
        data = {
            "email": self.user,
            "password": self.password,
            "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/"
        }
        self._request("POST", "https://auth-ac.my.com/auth?lang=ru&nosavelogin=0",
                      headers=self.auth_headers, data=data, jsonify=False)
        self.get_csrf()

    def post_create_segment(self):
        location = "/api/v2/remarketing/segments.json"
        return self._request("POST", location, json=segment_payload)

    def delete_segment(self, id_segment):
        location = f"/api/v2/remarketing/segments/{id_segment}.json"
        return self._request("DELETE", location, expected_status=204, jsonify=False)

    def get_segment_list(self):
        location = "api/v2/remarketing/segments.json"
        return self._request("GET", location, params='limit=500')

    def check_segment_id(self, segment_id):
        segment_list = self.get_segment_list()['items']
        for item_id in segment_list:
            if item_id['id'] == segment_id:
                return True
        return False

    def post_load_banner(self, file):
        location = "/api/v2/content/static.json"
        return self._request("POST", location, files=file)

    def get_url_id(self):
        location = "/api/v1/urls"
        params = {"url": fake.lexify(text="https://www.???????.com/")}
        return self._request("GET", location, params=params)

    def post_create_campaign(self, file):
        location = "/api/v2/campaigns.json"
        banner_id = self.post_load_banner(file)["id"]
        url_id = self.get_url_id()["id"]
        campaign_payload["banners"][0]["urls"]["primary"]["id"] = url_id
        campaign_payload["banners"][0]["content"]["image_240x400"]["id"] = banner_id
        return self._request("POST", location, json=campaign_payload)

    def delete_campaign(self, campaign_id):
        location = f"/api/v2/campaigns/{campaign_id}.json"
        return self._request("DELETE", location, expected_status=204, jsonify=False)

    def get_campaigns_list(self, status=None):
        location = "/api/v2/campaigns.json"
        params = {"_status__in": status, "limit": 250}
        return self._request("GET", location, params=params)

    def check_campaign(self, campaign_id, status):
        campaigns_list = self.get_campaigns_list(status)['items']
        for item_id in campaigns_list:
            if item_id['id'] == campaign_id:
                return True
        return False
