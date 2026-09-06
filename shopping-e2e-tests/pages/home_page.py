from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = BasePage.data_test("search-query")
    SEARCH_SUBMIT = BasePage.data_test("search-submit")
    SEARCH_RESET = BasePage.data_test("search-reset")
    SIGN_IN_LINK = BasePage.data_test("nav-sign-in")
    CART_LINK = BasePage.data_test("nav-cart")
    CART_QUANTITY = BasePage.data_test("cart-quantity")
    SORT_SELECT = BasePage.data_test("sort")
    PRODUCT_CARDS = (By.CSS_SELECTOR, 'a[data-test^="product-"]')
    PRODUCT_NAMES = (By.CSS_SELECTOR, '[data-test="product-name"]')

    def load(self, base_url):
        self.driver.get(base_url)
        self.find(self.PRODUCT_CARDS)
        return self

    def search(self, term):
        previous_names = self.product_names()
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_SUBMIT)
        self._wait_for_product_list_to_change(previous_names)
        return self

    def reset_search(self):
        previous_names = self.product_names()
        self.click(self.SEARCH_RESET)
        self._wait_for_product_list_to_change(previous_names)
        return self

    def _wait_for_product_list_to_change(self, previous_names):
        self.wait.until(lambda driver: self.product_names() != previous_names)

    def sort_by(self, value):
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def product_names(self):
        return [element.text.strip() for element in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def has_products(self):
        return len(self.driver.find_elements(*self.PRODUCT_CARDS)) > 0

    def click_product_by_name(self, name):
        for card in self.find_all(self.PRODUCT_CARDS):
            if name.strip().lower() in card.text.strip().lower():
                card.click()
                return
        raise ValueError(f"Product '{name}' not found on the current page")

    def go_to_sign_in(self):
        self.click(self.SIGN_IN_LINK)
        return self

    def open_cart(self):
        self.click(self.CART_LINK)
        return self

    def cart_quantity(self):
        if not self.is_visible(self.CART_QUANTITY, timeout=2):
            return 0
        return int(self.text_of(self.CART_QUANTITY))
