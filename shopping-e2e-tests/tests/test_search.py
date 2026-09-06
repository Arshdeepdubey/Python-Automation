import pytest

from pages.home_page import HomePage


@pytest.mark.smoke
def test_search_returns_matching_products(driver, base_url):
    home = HomePage(driver).load(base_url)

    home.search("pliers")

    names = home.product_names()
    assert names, "Expected at least one search result"
    assert all("pliers" in name.lower() for name in names)


def test_search_with_no_matches_shows_no_products(driver, base_url):
    home = HomePage(driver).load(base_url)

    home.search("no-such-product-xyz123")

    assert home.has_products() is False


def test_reset_search_restores_full_catalog(driver, base_url):
    home = HomePage(driver).load(base_url)
    full_catalog_count = len(home.product_names())

    home.search("pliers")
    assert len(home.product_names()) < full_catalog_count

    home.reset_search()
    assert len(home.product_names()) == full_catalog_count
