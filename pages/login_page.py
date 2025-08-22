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
        """Logs in to the application.
        Author:
            Prasad Kamble
        """
        self.page.wait_for_timeout(4000) 
        if self.username_selector.is_visible():
            self.username_selector.fill(username)
            self.password_selector.fill(password)
            self.login_button_selector.click()
            print("Login attempted.")
        else:
            print("Login page not visible, skipping login.")
