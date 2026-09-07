from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class CheckoutPage(BasePage):
    PRODUCT_TITLE = BasePage.data_test("product-title")
    CART_TOTAL = BasePage.data_test("cart-total")
    CONTINUE_SHOPPING = BasePage.data_test("continue-shopping")
    PROCEED_TO_SIGN_IN = BasePage.data_test("proceed-1")

    LOGIN_EMAIL = BasePage.data_test("email")
    LOGIN_PASSWORD = BasePage.data_test("password")
    LOGIN_SUBMIT = BasePage.data_test("login-submit")
    PROCEED_TO_BILLING_AS_USER = BasePage.data_test("proceed-2")

    GUEST_TAB = (By.LINK_TEXT, "Continue as Guest")
    GUEST_EMAIL = BasePage.data_test("guest-email")
    GUEST_FIRST_NAME = BasePage.data_test("guest-first-name")
    GUEST_LAST_NAME = BasePage.data_test("guest-last-name")
    GUEST_SUBMIT = BasePage.data_test("guest-submit")
    PROCEED_TO_BILLING_AS_GUEST = BasePage.data_test("proceed-2-guest")

    COUNTRY = BasePage.data_test("country")
    POSTAL_CODE = BasePage.data_test("postal_code")
    HOUSE_NUMBER = BasePage.data_test("house_number")
    STREET = BasePage.data_test("street")
    CITY = BasePage.data_test("city")
    STATE = BasePage.data_test("state")
    PROCEED_TO_PAYMENT = BasePage.data_test("proceed-3")

    PAYMENT_METHOD = BasePage.data_test("payment-method")
    FINISH_BUTTON = BasePage.data_test("finish")
    PAYMENT_SUCCESS_MESSAGE = BasePage.data_test("payment-success-message")

    def cart_total(self):
        return self.text_of(self.CART_TOTAL)

    def proceed_from_cart(self):
        self.click(self.PROCEED_TO_SIGN_IN)
        return self

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_SUBMIT)
        self.click(self.PROCEED_TO_BILLING_AS_USER)
        return self

    def checkout_as_guest(self, email, first_name, last_name):
        self.click(self.GUEST_TAB)
        self.type_text(self.GUEST_EMAIL, email)
        self.type_text(self.GUEST_FIRST_NAME, first_name)
        self.type_text(self.GUEST_LAST_NAME, last_name)
        self.click(self.GUEST_SUBMIT)
        self.click(self.PROCEED_TO_BILLING_AS_GUEST)
        return self

    def fill_address(self, country_code, postal_code, house_number, street, city, state):
        Select(self.find(self.COUNTRY)).select_by_value(country_code)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.type_text(self.HOUSE_NUMBER, house_number)
        self.type_text(self.STREET, street)
        self.type_text(self.CITY, city)
        self.type_text(self.STATE, state)
        return self

    def proceed_to_payment(self):
        self.click(self.PROCEED_TO_PAYMENT)
        return self

    def select_payment_method(self, value):
        Select(self.find(self.PAYMENT_METHOD)).select_by_value(value)
        return self

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)
        return self

    def payment_success_message(self):
        return self.text_of(self.PAYMENT_SUCCESS_MESSAGE)
