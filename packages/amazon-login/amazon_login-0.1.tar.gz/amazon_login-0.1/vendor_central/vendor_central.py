from vendor_central.vendor_login import VendorLogin
from utils.webdriver_actions import WebDriverActions
from utils.driver import get_default_driver


class VendorCentral:
    def __init__(
        self,
        username,
        password,
        login_link,
        logged_in_element,
        sender_email,
        recipient_emails,
        driver=None,
    ):
        if driver is None:
            self.driver = get_default_driver()
        else:
            self.driver = driver
        self.driver_actions = WebDriverActions(self.driver)
        self.login_module = VendorLogin(
            self.driver_actions,
            username,
            password,
            login_link,
            logged_in_element,
            sender_email,
            recipient_emails,
        )

    def login(self):
        return self.login_module.login()
