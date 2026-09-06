import pytest

from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


def _open_first_search_result(driver, base_url, term):
    home = HomePage(driver).load(base_url)
    home.search(term)
    home.click_product_by_name(home.product_names()[0])
    return ProductPage(driver)


@pytest.mark.smoke
def test_add_product_to_cart_updates_cart_count(driver, base_url):
    product = _open_first_search_result(driver, base_url, "pliers")

    product.add_to_cart()

    header = HomePage(driver)
    assert header.cart_quantity() == 1


def test_increasing_quantity_before_adding_updates_cart_count(driver, base_url):
    product = _open_first_search_result(driver, base_url, "pliers")

    product.increase_quantity(times=2)
    assert product.quantity() == "3"
    product.add_to_cart()

    header = HomePage(driver)
    assert header.cart_quantity() == 3


def test_cart_page_lists_added_product(driver, base_url):
    product = _open_first_search_result(driver, base_url, "pliers")
    product_name = product.name()
    product.add_to_cart()

    checkout = CheckoutPage(driver).load(base_url)

    assert product_name in checkout.text_of(checkout.PRODUCT_TITLE)
    assert checkout.cart_total()
