from pages.base_page import BasePage

class ConfigurationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.location_tab = self.page.get_by_role("tab", name="Locations")
        self.search_box = self.page.get_by_role('button', name='Search')
        self.search_location = self.page.get_by_role('textbox', name='Search location')
        self.table_path_locator = self.page.locator('td span.pointer-cursor')
        self.configuration = self.page.locator('button:has-text("Configuration")')