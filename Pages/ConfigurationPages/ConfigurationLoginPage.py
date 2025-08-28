class ConfigurationLoginPage():
    def __init__(self, page):
        self.page = page
        self.username_selector = self.page.get_by_role('textbox', name='Username')
        self.password_selector = self.page.get_by_role('textbox', name='Password')
        self.submit_button_selector = self.page.get_by_role('button', name='Submit')

    def navigate(self, url):
        """Navigate to a specific URL.
        
        Author:
            Prasad Kamble
        """
        self.page.goto(url)
    
    def configuration_login(self, username, password):
        """Logs in to the configuration page.
        Author:
            Prasad Kamble
        """
        self.username_selector.fill(username)
        self.password_selector.fill(password)
        self.password_selector.press("Enter")
        # self.submit_button_selector.click()
        
    def navigate_to_configuration(self, button_text):
        """Navigates to the configuration page by clicking the specified button.
        Author:
            Prasad Kamble
        """
        self.page.locator(f'button:has-text("{button_text}")').click()
        