from Pages.ConfigurationPages.ConfigurationLoginPage import ConfigurationLoginPage
from Pages.ConfigurationPages.ConfigurationPage import ConfigurationPage
from Utilites.ExcelRead.ConfigRead import ConfigUtils
from Utilites.UIUtils import UIUtils
from Pages.ConfigurationPages.CasinoManager import CasinoManager
from Utilites.APIs.ConfigurationAPIs import ConfigurationAPIs
from Utilites.Logs.LoggerUtils import LoggerUtils

class ConfigurationActions:
    def __init__(self, page, feature_name):
        self.page = page
        self.feature_name = feature_name
        self.configuration_page = ConfigurationPage(page)
        self.configuration_api = ConfigurationAPIs(feature_name)
        self.ui_utils = UIUtils(page)
        self.config_utils = ConfigUtils()
        self.config_utils.set_feature_name(feature_name)
        self.logger_utils = LoggerUtils(self.feature_name)

    def table_path_search(self, table_name):
        self.logger_utils.log(f"Searching for table path using table name: {table_name}")
        self.ui_utils.click_to_element(self.configuration_page.location_tab)
        self.logger_utils.log("Clicked location tab.")
        self.ui_utils.click_to_element(self.configuration_page.search_box)
        self.logger_utils.log("Clicked search box.")
        self.ui_utils.fill_element(self.configuration_page.search_location, table_name)
        self.logger_utils.log(f"Filled search location with table name: {table_name}")
        self.ui_utils.press_enter(self.configuration_page.search_location)
        self.logger_utils.log("Pressed enter in search location.")
        table_path = self.ui_utils.get_text(self.configuration_page.table_path_locator)
        self.logger_utils.log(f"Table path found for '{table_name}': {table_path}")
        return table_path
    
    def split_table_path(self, table_path):
        """
        Splits the table path string by '/' and returns a list of its parts.
        """
        self.logger_utils.log(f"Splitting table path: {table_path}")
        split_path = [part.strip() for part in table_path.split('/') if part.strip()]
        self.logger_utils.log(f"Split table path result: {split_path}")
        return split_path

    def drill_down(self, setup, table_ip):
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
        self.logger_utils.log(f"Starting drill_down for table_ip: {table_ip}")
        config_page = setup.context.new_page()
        config_page.goto(self.config_utils.get_ppApplication_Url())  
        self.logger_utils.log("Navigated to PP Application URL.")
        config_login = ConfigurationLoginPage(config_page)
        config_actions = ConfigurationActions(config_page, self.feature_name)
        configuration_page = ConfigurationPage(config_page)
        ui_utils = UIUtils(config_page)
        config_login.configuration_login(self.config_utils.get_username(), self.config_utils.get_password())
        self.logger_utils.log("Logged in to configuration page.")
        config_login.navigate_to_configuration("Configuration")
        self.logger_utils.log("Navigated to Configuration section.")
        config_page.wait_for_timeout(2000)

        table_info = self.configuration_api.get_table_info(table_ip)
        table_name = table_info.get("tableName")
        self.logger_utils.log(f"Fetched table info from API. Table name: {table_name}")

        # Search for table path in UI and split it
        table_path = config_actions.table_path_search(table_name)
        self.logger_utils.log(f"Table path from UI: {table_path}")
        split_path = config_actions.split_table_path(table_path)
        self.logger_utils.log(f"Split table path: {split_path}")
        ui_utils.click_to_element(configuration_page.apps_configuration)
        self.logger_utils.log("Clicked Apps Configuration.")
        with config_page.expect_popup() as page1_info:
            ui_utils.click_to_element(configuration_page.casino_manager)
            self.logger_utils.log("Clicked Casino Manager.")
        page1 = page1_info.value
        casino_manager = CasinoManager(page1)
        ui_utils = UIUtils(page1)
        site_name = split_path[1]
        ga_name = split_path[2]
        oa_name = split_path[3]
        pit_name = split_path[4]

        self.logger_utils.log(f"Clicking site: {site_name}, GA: {ga_name}, OA: {oa_name}, Pit: {pit_name}")
        ui_utils.click_to_element(casino_manager.site_button(site_name))
        ui_utils.click_to_element(casino_manager.ga_button(ga_name))
        ui_utils.click_to_element(casino_manager.oa_text(oa_name))
        ui_utils.click_to_element(casino_manager.pit_text(pit_name))
        self.logger_utils.log("Drill down navigation completed.")
        return page1

    def prepend_host_entry(self, hosts_path, new_entry):
        try:
            with open(hosts_path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith("#"):
                    insert_index = i
                    break
            lines.insert(insert_index, new_entry.strip())
            with open(hosts_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        except PermissionError:
            print(f"Permission denied: You must run as administrator to modify {hosts_path}")