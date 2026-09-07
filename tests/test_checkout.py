import pytest

from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

ADDRESS = {
    "country_code": "US",
    "postal_code": "10001",
    "house_number": "123",
    "street": "Main Street",
    "city": "New York",
    "state": "NY",
}


def _add_first_search_result_to_cart(driver, base_url, term):
    home = HomePage(driver).load(base_url)
    home.search(term)
    home.click_product_by_name(home.product_names()[0])
    ProductPage(driver).add_to_cart()


@pytest.mark.smoke
def test_logged_in_checkout_completes_successfully(driver, base_url, test_user):
    _add_first_search_result_to_cart(driver, base_url, "pliers")

    HomePage(driver).open_cart()
    checkout = CheckoutPage(driver)
    checkout.proceed_from_cart()
    checkout.login(test_user["email"], test_user["password"])
    checkout.fill_address(**ADDRESS)
    checkout.proceed_to_payment()
    checkout.select_payment_method("cash-on-delivery")
    checkout.finish_checkout()

    assert "payment was successful" in checkout.payment_success_message().lower()


def test_guest_checkout_completes_successfully(driver, base_url):
    _add_first_search_result_to_cart(driver, base_url, "pliers")

    HomePage(driver).open_cart()
    checkout = CheckoutPage(driver)
    checkout.proceed_from_cart()
    checkout.checkout_as_guest("guest.e2e@example.com", "Guest", "Shopper")
    checkout.fill_address(**ADDRESS)
    checkout.proceed_to_payment()
    checkout.select_payment_method("cash-on-delivery")
    checkout.finish_checkout()

    assert "payment was successful" in checkout.payment_success_message().lower()
