from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 20


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    @staticmethod
    def data_test(value):
        return By.CSS_SELECTOR, f'[data-test="{value}"]'

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text, clear=True):
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text.strip()

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_until_url_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
