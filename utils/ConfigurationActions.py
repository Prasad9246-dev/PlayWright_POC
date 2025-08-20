from pages.Configuration_Page import ConfigurationPage
from utils.UIUtils import UIUtils

class ConfigurationActions:
    def __init__(self, page):
        self.page = page
        self.configuration_page = ConfigurationPage(page)
        self.ui_utils = UIUtils(page)

    def table_path_search(self, table_name):
        self.ui_utils.click_to_element(self.configuration_page.location_tab)
        self.ui_utils.click_to_element(self.configuration_page.search_box)
        self.ui_utils.fill_element(self.configuration_page.search_location, table_name)
        self.ui_utils.press_enter(self.configuration_page.search_location)
        return self.ui_utils.get_text(self.configuration_page.table_path_locator)
    
    def split_table_path(self, table_path):
        """
        Splits the table path string by '/' and returns a list of its parts.
        """
        return [part.strip() for part in table_path.split('/') if part.strip()]