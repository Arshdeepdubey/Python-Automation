from .base_page import BasePage


class ProductPage(BasePage):
    NAME = BasePage.data_test("product-name")
    PRICE = BasePage.data_test("unit-price")
    QUANTITY_INPUT = BasePage.data_test("quantity")
    INCREASE_QUANTITY = BasePage.data_test("increase-quantity")
    DECREASE_QUANTITY = BasePage.data_test("decrease-quantity")
    ADD_TO_CART = BasePage.data_test("add-to-cart")
    CART_QUANTITY_BADGE = BasePage.data_test("cart-quantity")

    def name(self):
        return self.text_of(self.NAME)

    def price(self):
        return self.text_of(self.PRICE)

    def quantity(self):
        return self.find(self.QUANTITY_INPUT).get_attribute("value")

    def set_quantity(self, quantity):
        element = self.find(self.QUANTITY_INPUT)
        element.clear()
        element.send_keys(str(quantity))
        return self

    def increase_quantity(self, times=1):
        for _ in range(times):
            self.click(self.INCREASE_QUANTITY)
        return self

    def decrease_quantity(self, times=1):
        for _ in range(times):
            self.click(self.DECREASE_QUANTITY)
        return self

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)
        self.find(self.CART_QUANTITY_BADGE)
        return self
