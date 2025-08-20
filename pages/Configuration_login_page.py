from pages.base_page import BasePage

class ConfigurationLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.username_selector = self.page.get_by_role('textbox', name='Username')
        self.password_selector = self.page.get_by_role('textbox', name='Password')
        self.submit_button_selector = self.page.get_by_role('button', name='Submit')
        self.configuration = self.page.locator('button:has-text("Configuration")')

    def configuration_login(self, username, password):
        self.username_selector.fill(username)
        self.password_selector.fill(password)
        self.password_selector.press("Enter")
        # self.submit_button_selector.click()
        
    def navigate_to_configuration(self, button_text):
        self.page.locator(f'button:has-text("{button_text}")').click()