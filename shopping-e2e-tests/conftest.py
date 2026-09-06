import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "customer@practicesoftwaretesting.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "welcome01")


def pytest_addoption(parser):
    parser.addoption(
        "--no-headless",
        action="store_true",
        default=False,
        help="Run the browser with a visible window instead of headless.",
    )


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def test_user():
    return {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}


@pytest.fixture
def driver(request):
    headless = os.getenv("HEADLESS", "true").lower() == "true" and not request.config.getoption("--no-headless")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1024")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # The site's Angular app runs bot-fingerprint checks; a stock Selenium
    # Chrome exposes navigator.webdriver=true and other automation tells,
    # which can cause it to silently serve a stripped page. These flags
    # (plus the CDP override below) make the browser look like a regular
    # user's Chrome, which this practice site expects to be automated.
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )

    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    chrome_driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
    )
    chrome_driver.implicitly_wait(0)

    yield chrome_driver

    chrome_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        chrome_driver = item.funcargs.get("driver")
        if chrome_driver is not None:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            safe_name = item.name.replace("/", "_")
            chrome_driver.save_screenshot(os.path.join(screenshots_dir, f"{safe_name}.png"))
            with open(os.path.join(screenshots_dir, f"{safe_name}.html"), "w", encoding="utf-8") as f:
                f.write(chrome_driver.page_source)
