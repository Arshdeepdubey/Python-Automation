from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = BasePage.data_test("email")
    PASSWORD_INPUT = BasePage.data_test("password")
    SUBMIT_BUTTON = BasePage.data_test("login-submit")
    REGISTER_LINK = BasePage.data_test("register-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger, .alert-error, [role='alert']")

    def load(self, base_url):
        self.driver.get(f"{base_url}/auth/login")
        return self

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
        return self

    def error_message(self):
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=5)

    def go_to_register(self):
        self.click(self.REGISTER_LINK)
        return self
