from pages.base_page import BasePage
from playwright.sync_api import TimeoutError

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.username_selector = self.page.get_by_role('textbox', name='Username')
        self.password_selector = self.page.get_by_role('textbox', name='Password')
        self.login_button_selector = self.page.get_by_role('button', name='Login')

    def navigate(self, url):
        self.page.goto(url)

    def login(self, username, password):
        try:
            # Wait up to 2 seconds for the username field to be visible
            self.username_selector.wait_for(state="visible", timeout=2000)
            self.username_selector.fill(username)
            self.password_selector.fill(password)
            self.login_button_selector.click()
        except TimeoutError:
            # Username field not visible, skip login
            print("Username field not visible, skipping login.")
