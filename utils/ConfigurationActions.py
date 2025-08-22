from pages.ConfigurationLoginPage import ConfigurationLoginPage
from pages.ConfigurationPage import ConfigurationPage
from utils.config_read import ConfigUtils
from utils.UIUtils import UIUtils
from pages.CasinoManager import CasinoManager

class ConfigurationActions:
    def __init__(self, page):
        self.page = page
        self.configuration_page = ConfigurationPage(page)
        self.ui_utils = UIUtils(page)
        self.config_utils = ConfigUtils()

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

    def drill_down(self, tbd, setup, table_ip):
        """
        Navigates through the configuration UI to locate a table by its IP.

        Args:
            tbd: API access object.
            setup: Playwright setup/context.
            table_ip: Table IP address.

        Returns:
            page1: Casino Manager popup page object.
        
        Author:
            Prasad Kamble
        """
        config_page = setup.context.new_page()
        config_page.goto(self.config_utils.get_ppApplication_Url())  

        config_login = ConfigurationLoginPage(config_page)
        config_actions = ConfigurationActions(config_page)
        configuration_page = ConfigurationPage(config_page)
        ui_Utils = UIUtils(config_page)
        config_login.configuration_login(self.config_utils.get_username(), self.config_utils.get_password())
        config_login.navigate_to_configuration("Configuration")
        config_page.wait_for_timeout(2000)

        # Get table info and name from API
        table_info = tbd.Configuration_API.get_table_info(table_ip)
        table_name = table_info.get("tableName")
        print(f"Table Name: {table_name}")

        # Search for table path in UI and split it
        table_path = config_actions.table_path_search(table_name)
        split_path = config_actions.split_table_path(table_path)
        print(f"Table Path: {table_path}")
        print(f"Split Table Path: {split_path}")
        ui_Utils.click_to_element(configuration_page.apps_configuration)
        with config_page.expect_popup() as page1_info:
            ui_Utils.click_to_element(configuration_page.casino_manager)
        page1 = page1_info.value
        casino_manager = CasinoManager(page1)
        ui_Utils = UIUtils(page1)
        # Store split_path values in variables for clarity
        site_name = split_path[1]
        ga_name = split_path[2]
        oa_name = split_path[3]
        pit_name = split_path[4]

        ui_Utils.click_to_element(casino_manager.site_button(site_name))
        ui_Utils.click_to_element(casino_manager.ga_button(ga_name))
        ui_Utils.click_to_element(casino_manager.oa_text(oa_name))
        ui_Utils.click_to_element(casino_manager.pit_text(pit_name))
        return page1