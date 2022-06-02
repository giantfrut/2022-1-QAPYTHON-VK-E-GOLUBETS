
import allure
import pytest
from base import BaseCase

from ui.locators.locators import AuthorizedPageLocators
from utils.builder import Builder


@pytest.mark.UI
@allure.feature('UI auth tests')
class TestAuthUI(BaseCase):
    @allure.description(
        """
        Test fields validation on the login page
        """
    )
    def test_auth_fields_validation(self, login_page):
        assert login_page.check_validation(login_page.locators.USERNAME_LOCATOR)
        assert login_page.check_validation(login_page.locators.PASSWORD_LOCATOR)

    @allure.description(
        """
        Test login with correct login and password
        """
    )
    def test_correct_credentials(self, login_page, authorized_page, admin):
        login_page.auth(admin.username, admin.password)
        assert authorized_page.find(authorized_page.locators.LOGOUT_BUTTON)

    @allure.description(
        """
        Test login with block
        """
    )
    def test_auth_blocked(self, login_page, mysql_client):
        user = Builder.user(access=0)
        mysql_client.add_user_db(user)
        login_page.auth(user.username, user.password)
        assert login_page.find_text(login_page.locators.ERROR_MESSAGE) == 'Ваша учетная запись заблокирована'

    @allure.description(
        """
        Test login with incorrect password
        """
    )
    def test_auth_incorrect_password(self, login_page, admin):
        login_page.auth(admin.username, admin.password + "1")
        assert login_page.find_text(login_page.locators.ERROR_MESSAGE) == 'Invalid username or password'

    @allure.description(
        """
        Test check user active after login
        """
    )
    def test_user_active(self, login_page, mysql_client):
        user = Builder.user()
        mysql_client.add_user_db(user)
        login_page.auth(user.username, user.password)
        assert mysql_client.select_db(user.username).active == 1

    @allure.description(
        """
        Test check that can go to registration page
        """
    )
    def test_go_to_registration(self, login_page):
        login_page.go_to_registration_page()
        assert self.driver.current_url == 'http://127.0.0.1:8080/reg'


@pytest.mark.UI
@allure.feature('UI registration tests')
class TestRegistrationUI(BaseCase):
    @allure.description(
        """
        Test fields validation on registration page
        """
    )
    def test_reg_fields_validation(self, registration_page):
        assert registration_page.reg_check_validation()

    @allure.description(
        """
        Test registration with normal user data
        """
    )
    def test_correct_registration(self, registration_page, mysql_client, authorized_page):
        user = Builder.user()
        registration_page.registration(user, confirm_password=user.password)
        assert mysql_client.select_db(user.username)
        assert authorized_page.find(authorized_page.locators.LOGOUT_BUTTON)

    @allure.description(
        """
        Test registration without surname
        """
    )
    def test_registration_without_surname(self, registration_page, mysql_client, authorized_page):
        user = Builder.user(surname=None)
        registration_page.registration(user, confirm_password=user.password)
        assert mysql_client.select_db(user.username)
        assert authorized_page.find(authorized_page.locators.LOGOUT_BUTTON)

    @allure.description(
        """
        Test registration without accept agreement
        """
    )
    def test_no_accept_registration(self, registration_page, mysql_client):
        user = Builder.user()
        registration_page.registration(user, confirm_password=user.password, accept=False)
        assert mysql_client.select_db(user.username) is None
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration without confirm password
        """
    )
    def test_no_confirm_password(self, registration_page, mysql_client):
        user = Builder.user()
        registration_page.registration(user, confirm_password="PASS")
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == 'Passwords must match'
        assert mysql_client.select_db(user.username) is None
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration with password length = 256
        """
    )
    def test_long_password(self, registration_page, mysql_client):
        user = Builder.user(password_length=256)
        registration_page.registration(user, confirm_password=user.password)
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == 'Invalid password length'
        assert mysql_client.select_db(user.username) is None
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration new user with already exist username
        """
    )
    def test_username_exists_registration(self, registration_page, mysql_client, admin):
        user = Builder.user(username=admin.username)
        registration_page.registration(user, confirm_password=user.password)
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == "User already exist"
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration new user with already exist email address
        """
    )
    def test_email_exists_registration(self, registration_page, admin):
        user = Builder.user(email=admin.email)
        registration_page.registration(user, confirm_password=user.password)
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == "Email address already exist"
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration with invalid email (only @mail.ru)
        """
    )
    def test_invalid_email_registration(self, registration_page):
        user = Builder.user(email='@mail.ru')
        registration_page.registration(user, confirm_password=user.password)
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == "Invalid email address"
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test registration without @ part of email
        """
    )
    def test_email_without_at(self, registration_page):
        user = Builder.user(email='username')
        registration_page.registration(user, confirm_password=user.password)
        assert registration_page.find_text(registration_page.locators.ERROR_MESSAGE) == "Invalid email address"
        assert self.driver.current_url == registration_page.REG_URL

    @allure.description(
        """
        Test check that user can go to login page
        """
    )
    def test_go_to_login_page(self, registration_page):
        registration_page.go_to_login_page()
        assert self.driver.current_url == 'http://127.0.0.1:8080/login'


@pytest.mark.UI
@allure.feature('UI main page tests')
class TestMainPageUI(BaseCase):
    @allure.description(
        """
        Test user logout
        """
    )
    def test_user_logout(self, auth_page, authorized_page):
        authorized_page.click(authorized_page.locators.LOGOUT_BUTTON)
        assert self.driver.current_url == "http://127.0.0.1:8080/login"

    @allure.description(
        """
        Test user active after logout
        """
    )
    def test_logout_active(self, auth_page, admin, authorized_page, mysql_client):
        authorized_page.click(authorized_page.locators.LOGOUT_BUTTON)
        assert mysql_client.select_db(admin.username).active == 0

    @allure.description(
        """
        Test check get vk_id info 
        """
    )
    def test_vk_id_info(self, auth_page, api_client, admin, authorized_page):
        api_client.add_vk_id(admin.username)
        vk_id = api_client.get_vk_id(admin.username).json()['vk_id']
        self.driver.refresh()
        assert authorized_page.find_text(authorized_page.locators.VK_ID_LOCATOR) == f"VK ID: {vk_id}"

    @allure.description(
        """
        Test check central links can open in new tab
        """
    )
    @pytest.mark.parametrize('central_button, expected_result',
                             [
                                 (AuthorizedPageLocators.API_BUTTON, 'https://en.wikipedia.org/wiki/API'),
                                 (AuthorizedPageLocators.INTERNET_BUTTON,
                                  'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'),
                                 (AuthorizedPageLocators.SMTP_BUTTON, 'https://ru.wikipedia.org/wiki/SMTP')
                             ])
    def test_check_central_links(self, auth_page, authorized_page, central_button, expected_result):
        authorized_page.click(central_button)
        authorized_page.switch_to_next_window()
        assert self.driver.current_url == expected_result

    @allure.description(
        """
        Test go home buttons 
        """
    )
    @pytest.mark.parametrize('home_button, expected_result',
                             [
                                 (AuthorizedPageLocators.BRAND_BUTTON, 'http://127.0.0.1:8080/welcome/'),
                                 (AuthorizedPageLocators.HOME_BUTTON, 'http://127.0.0.1:8080/welcome/'),
                                 (AuthorizedPageLocators.PYTHON_BUTTON, 'https://www.python.org/')
                             ])
    def test_menu_click_buttons(self, auth_page, authorized_page, home_button, expected_result):
        authorized_page.click(home_button)
        assert self.driver.current_url == expected_result

    @allure.description(
        """
        Test navbar buttons can open in new tab 
        """
    )
    @pytest.mark.parametrize('parent_button, navbar_button, expected_result',
                             [
                                 (AuthorizedPageLocators.PYTHON_BUTTON, AuthorizedPageLocators.PYTHON_HISTORY_BUTTON,
                                  "https://en.wikipedia.org/wiki/History_of_Python"),
                                 (AuthorizedPageLocators.PYTHON_BUTTON, AuthorizedPageLocators.FLASK_BUTTON,
                                  "https://flask.palletsprojects.com/en/1.1.x/#"),
                                 (AuthorizedPageLocators.LINUX_BUTTON, AuthorizedPageLocators.CENTOS_BUTTON,
                                  "https://www.centos.org/download/"),
                                 (AuthorizedPageLocators.NETWORK_BUTTON, AuthorizedPageLocators.WIRESHARK_NEWS,
                                  "https://www.wireshark.org/news/"),
                                 (AuthorizedPageLocators.NETWORK_BUTTON, AuthorizedPageLocators.WIRESHARK_DOWNLOAD,
                                  "https://www.wireshark.org/#download"),
                                 (AuthorizedPageLocators.NETWORK_BUTTON, AuthorizedPageLocators.TCPDUMP_EXAMPLE,
                                  "https://hackertarget.com/tcpdump-examples/")

                             ])
    def test_navbar_buttons(self, auth_page, authorized_page, parent_button, navbar_button, expected_result):
        authorized_page.hover_on_element(parent_button)
        authorized_page.click(navbar_button)
        authorized_page.switch_to_next_window()
        assert self.driver.current_url == expected_result  # python history в текущем окне, fedora

    @allure.description(
        """
        Test check python fact in page bottom
        """
    )
    def test_python_facts(self, auth_page, authorized_page):
        assert authorized_page.find(authorized_page.locators.PYTHON_FACT)
