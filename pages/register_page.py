from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class RegisterPage(BasePage):
    FIRST_NAME = BasePage.data_test("first-name")
    LAST_NAME = BasePage.data_test("last-name")
    DOB = BasePage.data_test("dob")
    COUNTRY = BasePage.data_test("country")
    POSTAL_CODE = BasePage.data_test("postal_code")
    HOUSE_NUMBER = BasePage.data_test("house_number")
    STREET = BasePage.data_test("street")
    CITY = BasePage.data_test("city")
    STATE = BasePage.data_test("state")
    PHONE = BasePage.data_test("phone")
    EMAIL = BasePage.data_test("email")
    PASSWORD = BasePage.data_test("password")
    SUBMIT_BUTTON = BasePage.data_test("register-submit")

    def load(self, base_url):
        self.driver.get(f"{base_url}/auth/register")
        return self

    def register(self, user):
        self.type_text(self.FIRST_NAME, user["first_name"])
        self.type_text(self.LAST_NAME, user["last_name"])
        self.type_text(self.DOB, user["dob"])
        Select(self.find(self.COUNTRY)).select_by_value(user["country_code"])
        self.type_text(self.POSTAL_CODE, user["postal_code"])
        self.type_text(self.HOUSE_NUMBER, user["house_number"])
        self.type_text(self.STREET, user["street"])
        self.type_text(self.CITY, user["city"])
        self.type_text(self.STATE, user["state"])
        self.type_text(self.PHONE, user["phone"])
        self.type_text(self.EMAIL, user["email"])
        self.type_text(self.PASSWORD, user["password"])
        self.click(self.SUBMIT_BUTTON)
        return self
