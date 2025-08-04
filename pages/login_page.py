from pages.base_page import BasePage
from playwright.sync_api import TimeoutError

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def login(self, username, password):
        try:
            # Wait up to 2 seconds for the username field to be visible
            self.page.get_by_role('textbox', name='Username').wait_for(state="visible", timeout=2000)
            self.page.get_by_role('textbox', name='Username').fill(username)
            self.page.get_by_role('textbox', name='Password').fill(password)
            self.page.get_by_role('button', name='Login').click()
        except TimeoutError:
            # Username field not visible, skip login
            print("Username field not visible, skipping login.")
