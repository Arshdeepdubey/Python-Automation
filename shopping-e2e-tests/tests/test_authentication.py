import pytest

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.test_data import new_registration_user


@pytest.mark.smoke
def test_login_with_valid_credentials_redirects_to_account(driver, base_url, test_user):
    login = LoginPage(driver).load(base_url)

    login.login(test_user["email"], test_user["password"])

    login.wait_until_url_contains("/account")
    assert "/account" in driver.current_url


def test_login_with_invalid_credentials_shows_error(driver, base_url):
    login = LoginPage(driver).load(base_url)

    login.login("nobody@example.com", "wrong-password")

    assert login.has_error()
    assert "email or password" in login.error_message().lower() or login.error_message() != ""


def test_new_user_can_register(driver, base_url):
    register = RegisterPage(driver).load(base_url)
    user = new_registration_user()

    register.register(user)

    register.wait_until_url_contains("/auth/login")
    assert "/auth/login" in driver.current_url
