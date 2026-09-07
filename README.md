# Python Automation

[![E2E Tests](https://github.com/Arshdeepdubey/Python-Automation/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/Arshdeepdubey/Python-Automation/actions/workflows/e2e-tests.yml)

End-to-end UI test automation, written in Python with Selenium and pytest, against
[Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com) — an
open-source e-commerce demo app ([testsmith-io/practice-software-testing](https://github.com/testsmith-io/practice-software-testing))
built specifically for automation practice.

## About

This repo is a Selenium + pytest E2E suite exercising the core shopping flows of a
real (if intentionally practice-oriented) Angular single-page e-commerce app: catalog
search, cart, authentication, and full checkout as both a registered user and a guest.
It follows the Page Object Model, keys every locator off the site's stable `data-test`
attributes rather than CSS/XPath guesswork, and runs headlessly on every push and pull
request via GitHub Actions, with HTML reports and failure screenshots published as
workflow artifacts.

## Tech stack

| Layer              | Tool                                                              |
|---------------------|--------------------------------------------------------------------|
| Language            | Python 3.11                                                       |
| Browser automation  | [Selenium 4](https://www.selenium.dev/) (WebDriver)               |
| Driver management   | [webdriver-manager](https://pypi.org/project/webdriver-manager/) (auto-resolves the matching chromedriver) |
| Test runner         | [pytest](https://pytest.org/) + [pytest-rerunfailures](https://pypi.org/project/pytest-rerunfailures/) (rerun-on-flake) |
| Reporting           | [pytest-html](https://pypi.org/project/pytest-html/) (self-contained HTML report per run) |
| Config              | [python-dotenv](https://pypi.org/project/python-dotenv/) (`.env` for base URL, credentials, headless toggle) |
| Design pattern      | Page Object Model — one class per page under [`pages/`](pages)   |
| CI/CD               | GitHub Actions ([`.github/workflows/e2e-tests.yml`](.github/workflows/e2e-tests.yml)) |
| Diagnostics         | Automatic screenshot + page-source dump on failure (saved to `screenshots/`) |

## Setup

```bash
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
| `test_checkout.py`          | Full checkout as a guest (logged-in checkout is currently skipped — see below) |

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
- After `add_to_cart()`, the header badge updates client-side before the cart is
  necessarily persisted server-side. Navigating to checkout with a hard page reload
  right after can race that persistence — reliably enough to fail in CI, where network
  latency to the live site is higher than on a local connection. Tests reach checkout
  via the in-app cart link (`HomePage.open_cart()`) instead of a full-page navigation,
  which reuses the already-loaded cart state and sidesteps the race.
- The documented demo login (`customer@practicesoftwaretesting.com`) is a public
  credential shared by every automation script and tutorial that uses this site, so its
  account state is effectively contested global state — an in-flight edit from an
  unrelated script elsewhere can make a state-mutating flow like checkout intermittently
  time out for reasons that have nothing to do with this suite's code. Where a shared
  login isn't required, tests register their own fresh, uniquely-named user instead
  (via `RegisterPage` / `utils.test_data.new_registration_user()`).

## Known flaky test: logged-in checkout

`test_checkout.py::test_logged_in_checkout_completes_successfully` is currently
`@pytest.mark.skip`ped. It failed in CI at three different steps across three separate
fix attempts — a checkout-page reload racing cart persistence, a payment-step timeout
tied to the shared demo account, and finally the home page itself failing to render
right after registering a fresh account — while every other test in the same runs,
including the guest checkout right next to it, passed. That pattern (a different
failure point each time, nothing else in the run affected) points to live-site or
bot-heuristic variance under the CI runner's network conditions rather than a bug in
this suite's code, so it's quarantined rather than chased further. Re-enable it (drop
the `skip` marker) if the site's CI-time reliability improves, or if this suite moves
to a stubbed/self-hosted instance of the app instead of the public live site.

## CI/CD

A GitHub Actions workflow ([`.github/workflows/e2e-tests.yml`](.github/workflows/e2e-tests.yml))
runs the full suite headlessly on every push to any branch, every pull request, and on
demand. It installs dependencies, runs `pytest` against the live site, and uploads the
HTML report (and failure screenshots, if any) as workflow artifacts.

## Why this site

`demo.opencart.com` was considered but sits behind Cloudflare bot-verification, which
blocks Selenium the same way it blocks any other bot — so it was ruled out in favor of a
site built for this purpose, with stable `data-test` locators throughout.
