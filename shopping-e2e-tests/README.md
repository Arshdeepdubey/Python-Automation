# Shopping E2E Tests

Selenium + pytest end-to-end test suite for [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com),
an open-source demo shopping app purpose-built for automation practice.

## Stack

- **Selenium 4** (WebDriver) driving Chrome via `webdriver-manager` (auto-downloads the matching chromedriver)
- **pytest** as the test runner, with `pytest-html` for HTML reports
- Page Object Model — one class per page under [`pages/`](pages), keyed off the site's `data-test` attributes
- Automatic screenshot-on-failure (saved to `screenshots/`)

## Setup

```bash
cd shopping-e2e-tests
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Google Chrome must be installed locally. Configuration is read from environment
variables (see `.env.example` — copy it to `.env` to override defaults):

| Variable             | Default                                  | Purpose                              |
|----------------------|-------------------------------------------|---------------------------------------|
| `BASE_URL`           | `https://practicesoftwaretesting.com`     | Site under test                       |
| `HEADLESS`           | `true`                                    | Run Chrome headless                   |
| `TEST_USER_EMAIL`    | `customer@practicesoftwaretesting.com`    | Existing demo account (login tests)   |
| `TEST_USER_PASSWORD` | `welcome01`                               | Password for the above (public demo credentials, documented at [testsmith-io.github.io](https://testsmith-io.github.io/practice-software-testing/#/)) |

## Running the tests

```bash
pytest                      # full suite, headless
pytest --no-headless        # watch it run in a visible browser
pytest -m smoke             # just the smoke subset
pytest tests/test_cart.py   # a single file
```

An HTML report is written to `reports/report.html` after every run.

## What's covered

| File                        | Scenarios                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `test_search.py`            | Search returns matching products, no-match search shows nothing, reset restores the catalog |
| `test_cart.py`              | Add to cart updates the header badge, quantity selector before adding, cart page reflects the added product |
| `test_authentication.py`    | Valid login, invalid login error, new user registration                  |
| `test_checkout.py`          | Full checkout as a logged-in user, full checkout as a guest               |

## Notes on this site's behavior (why the page objects look the way they do)

- The Angular app **debounces search/filter re-renders**; page objects wait for the
  product list content to actually change rather than just being "present" in the DOM.
- Both guest and logged-in checkout have an **intermediate "Proceed to checkout"
  confirmation step** (`proceed-2-guest` / `proceed-2`) before the billing address form
  becomes visible — easy to miss since the address fields already exist in the DOM,
  just hidden.
- Registration is rejected with "password has appeared in a data leak" for common
  passwords (backend leak-check) — generated test users use a randomized password.
- The site auto-fills street/city/state from a postcode lookup after a short debounce;
  page objects always explicitly type these fields after the postal code/house number,
  so the intended values win regardless of the lookup's timing.
