from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverActions:
    def __init__(self, driver, wait_time=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, wait_time)

    def enter_text(self, by_criterion, criterion_value, text):
        element = self.wait.until(
            EC.presence_of_element_located((by_criterion, criterion_value))
        )
        element.clear()
        element.send_keys(text)

    def click_element(self, by_criterion, criterion_value, index=0):
        elements = self.wait.until(
            EC.presence_of_all_elements_located((by_criterion, criterion_value))
        )
        elements[index].click()

    def get_session_cookies(self):
        """Fetch session cookies."""
        cookies = self.driver.get_cookies()
        session_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
        return session_cookies
