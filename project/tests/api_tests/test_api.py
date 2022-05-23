import allure
import pytest

from tests.api_tests.base import BaseApi
from utils.builder import Builder


@allure.feature('Base API tests')
@pytest.mark.API
class TestApi(BaseApi):
    @allure.description(
        """
        Test get app status 
        """
    )
    def test_check_status(self):
        resp = self.api_client.get_status()
        assert resp.json()['status'] == 'ok'
        assert resp.status_code == 200

    @allure.description(
        """
        Test get user vk_id
        """
    )
    def test_get_vk_id(self):
        user = Builder.user()
        self.api_client.add_vk_id(user.username)
        resp = self.api_client.get_vk_id(user.username)
        assert resp.json()['vk_id']
        assert resp.status_code == 200


#      "masha sima and zhenya are little funny cute fury kittens"

@allure.feature('API registration tests')
@pytest.mark.API
class TestApiRegistration(BaseApi):
    @allure.description(
        """
        Test positive add user 
        """
    )
    @pytest.mark.parametrize(
        "user",
        [
            (Builder.user(username_length=15, password="t", email="t@u.ru")),
            (Builder.user(username_length=15, password="t", email="t1@u.ru")),
            (Builder.user(username_length=6, password_length=10, email_length=10)),
            (Builder.user(username_length=16, password_length=255, email_length=64)),
            (Builder.user(username_length=10, password_length=255, email_length=10))
        ]
    )
    def test_add_user_correct(self, authorized_api, user):
        resp = self.api_client.add_user(user)

        assert resp.json()['detail'] == 'User was added'
        assert self.mysql_client.select_db(user.username)
        assert resp.status_code == 200  # код 210

    @allure.description(
        """
        Test negative add user 
        """
    )
    @pytest.mark.parametrize(
        "user",
        [
            (Builder.user(username_length=256, password_length=10, email_length=10)),  # пустой пользователь баг
            (Builder.user(username=' ', password=' ', email=' ')),
            (Builder.user(username_length=10, password_length=256, email_length=128))
        ]
    )
    def test_add_user_incorrect(self, authorized_api, user):
        resp = self.api_client.add_user(user)
        assert resp.json()['detail'] != f'User was added'
        assert self.mysql_client.select_db(user.username) is None
        assert resp.status_code == 400

    @allure.description(
        """
        Test add new user with exist username
        """
    )
    def test_add_user_exist(self, authorized_api, admin):
        user = Builder.user(username=admin.username)
        # self.mysql_client.add_user_db(user)
        resp = self.api_client.add_user(user)
        assert resp.json()['detail'] == 'User already exists'
        assert resp.status_code == 400

    @allure.description(
        """
        Test add new user with exist email
        """
    )
    def test_add_email_exist(self, authorized_api, admin):
        user = Builder.user(email=admin.email)
        resp = self.api_client.add_user(user)
        assert resp.json()['detail'] == 'User already exists'
        assert resp.status_code == 400


@allure.feature('API login tests')
@pytest.mark.API
class TestApiAuth(BaseApi):
    @allure.description(
        """
        Test login exist user
        """
    )
    def test_user_auth_exist(self, admin):
        resp = self.api_client.post_login(admin.username, admin.password)
        assert self.mysql_client.select_db(admin.username).active == 1
        assert resp.status_code == 200

    @allure.description(
        """
        Test login non exist user
        """
    )
    def test_user_auth_non_exist(self):
        user = Builder.user()
        resp = self.api_client.post_login(user.username, user.password)
        assert resp.status_code == 401

    @allure.description(
        """
        Test login with incorrect password
        """
    )
    def test_user_incorrect_password(self, admin):
        resp = self.api_client.post_login(admin.username, admin.password + "1")
        assert resp.status_code == 401

    @allure.description(
        """
        Test login without symbols 
        """
    )
    def test_user_auth_null(self):
        resp = self.api_client.post_login("", "")
        assert resp.status_code == 401  # bug

    @allure.description(
        """
        Test login with space 
        """
    )
    def test_user_auth_spaces(self):
        resp = self.api_client.post_login(" ", " ")
        assert resp.status_code == 401  # bug

    @allure.description(
        """
        Test login with max + 1 length username
        """
    )
    def test_user_max(self):
        user = Builder.user(username_length=17)
        resp = self.api_client.post_login(user.username, user.password)  # max value
        assert resp.status_code == 401  # bug

    @allure.description(
        """
        Test login user with block access 
        """
    )
    def test_auth_blocked(self):
        user = Builder.user(access=0)
        self.mysql_client.add_user_db(user)
        resp = self.api_client.post_login(user.username, user.password)
        assert resp.status_code == 401

    @allure.description(
        """
        Test user logout 
        """
    )
    def test_logout(self, authorized_api, admin):
        resp = self.api_client.logout()
        assert resp.status_code == 200
        assert self.mysql_client.select_db(admin.username).active == 0


@allure.feature('API user tests')
@pytest.mark.API
class TestApiUser(BaseApi):
    @allure.description(
        """
        Test block user with authorized_api
        """
    )
    def test_block_user_auth(self, authorized_api):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.block_user(user.username)
        assert resp.status_code == 200
        assert self.mysql_client.select_db(user.username).access == 0

    @allure.description(
        """
        Test block user without authorized_api
        """
    )
    def test_block_user_non_auth(self):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.block_user(user.username)
        assert resp.status_code == 401
        assert self.mysql_client.select_db(user.username).access == 1

    @allure.description(
        """
        Test unblock user with authorized_api
        """
    )
    def test_unblock_user(self, authorized_api):
        user = Builder.user(access=0)
        self.mysql_client.add_user_db(user)
        resp = self.api_client.unblock_user(user.username)
        assert resp.status_code == 200
        assert self.mysql_client.select_db(user.username).access == 1

    @allure.description(
        """
        Test unblock user without authorized api
        """
    )
    def test_unblock_user_non_auth(self):
        user = Builder.user(access=0)
        self.mysql_client.add_user_db(user)
        resp = self.api_client.unblock_user(user.username)
        assert resp.status_code == 401
        assert self.mysql_client.select_db(user.username).access == 0

    @allure.description(
        """
        Test delete exist user 
        """
    )
    def test_delete_user_exists(self, authorized_api):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.delete_user(user.username)
        assert resp.status_code == 204
        assert self.mysql_client.select_db(user.username) is None

    @allure.description(
        """
        Test delete non exist user 
        """
    )
    def test_delete_user_non_exists(self, authorized_api):
        user = Builder.user()
        resp = self.api_client.delete_user(user.username)
        assert resp.status_code == 404

    @allure.description(
        """
        Test normal change user password
        """
    )
    def test_change_password(self, authorized_api):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.change_user_password(user.username, "1")
        assert self.mysql_client.select_db(user.username).password == '1'
        assert resp.status_code == 200

    @allure.description(
        """
        Test change repeat DB password
        """
    )
    def test_change_password_repeat(self, authorized_api):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.change_user_password(user.username, user.password)
        assert resp.status_code == 400

    @allure.description(
        """
        Test change password to None
        """
    )
    def test_change_password_incorrect(self, authorized_api):
        user = Builder.user()
        self.mysql_client.add_user_db(user)
        resp = self.api_client.change_user_password(user.username, "")
        assert self.mysql_client.select_db(user.username).password == user.password
        assert resp.status_code == 400
