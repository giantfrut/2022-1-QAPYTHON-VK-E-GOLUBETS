import logging
import faker
import requests
import allure
from urllib.parse import urljoin

MAX_RESPONSE_LENGTH = 300
logger = logging.getLogger('test')
fake = faker.Faker()


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

        self.session = requests.Session()
        self.headers = None

    @staticmethod
    def log_request(url, method, json):
        logger.info(
            f"Request:\n"
            f"Method: {method}\n"
            f"Url: {url}\n"
            f"Data: {json}\n"
        )

    @staticmethod
    def log_response(response):
        logger.info(
            f"Response status: {response.status_code}\n"
            f"Response data: {response.text}\n"
        )

    @allure.step("Send {method} request to {location}, json: {json}")
    def _request(self, method, location, headers=None, files=None, data=None, json=None, params=None, jsonify=True):
        url = urljoin(self.base_url, location)
        headers = headers or self.headers
        self.log_request(url, method, json)
        response = self.session.request(method, url, headers=headers, files=files, data=data, json=json, params=params)

        # if response.status_code != expected_status:
        #     raise ResponseStatusCodeException(f'Got {response.status_code} {response.request} for URL "{url}"')
        self.log_response(response)

        if jsonify:
            return response.json()
        return response

    @allure.step("API login with {login} and {password}")
    def post_login(self, login, password):
        location = "login"
        data = {
            "username": login,
            "password": password,
        }
        return self._request("POST", location, json=data, jsonify=False)

    @allure.step("API add new user: {user}")
    def add_user(self, user):
        location = "api/user"
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "name": user.name,
            "surname": user.surname,
            "middlename": user.middle_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
        return self._request("POST", location, headers=headers, json=body, jsonify=False)

    @allure.step("API go logout")
    def logout(self):
        location = "logout"
        return self._request("GET", location, jsonify=False)

    @allure.step("API get status")
    def get_status(self):
        location = "status"
        return self._request("GET", location, jsonify=False)

    @allure.step("Mock add vk id for {username}")
    def add_vk_id(self, username):
        location = f"http://127.0.0.1:5000/create_vk_id/{username}"
        return self.session.request("POST", location)

    @allure.step("Mock get vk id for {username}")
    def get_vk_id(self, username):
        location = f"http://127.0.0.1:5000/vk_id/{username}"
        return self.session.request("GET", location)

    @allure.step("API delete user with {username}")
    def delete_user(self, username):
        location = f"api/user/{username}"
        return self._request("DELETE", location, jsonify=False)

    @allure.step("Set user {username} new password: {password}")
    def change_user_password(self, username, password):
        location = f"api/user/{username}/change-password"
        data = {
            "password": password
        }
        return self._request("PUT", location, json=data, jsonify=False)

    @allure.step("Block user {username}")
    def block_user(self, username):
        location = f"api/user/{username}/block"
        return self._request("POST", location, jsonify=False)

    @allure.step("Unblock user {username}")
    def unblock_user(self, username):
        location = f"api/user/{username}/accept"
        return self._request("POST", location, jsonify=False)
