from tests.BaseTest import BaseTest
import allure
from pages.Configuration_login_page import ConfigurationLoginPage
from utils.ConfigurationActions import ConfigurationActions


@allure.feature("Buy-In Feature")
@allure.story("TEST-1999: Rated Buy-In")
@allure.title("TEST-1999 Rated Buy-In Test")
def test_1999(setup):
    # Initialize base test and page objects
    base_test = BaseTest(setup, "TEST-1999")
    config_page = setup.context.new_page()
    config_page.goto(base_test.base_url)

    # Login to configuration
    config_login = ConfigurationLoginPage(config_page)
    config_actions = ConfigurationActions(config_page)
    config_login.configuration_login(base_test.username, base_test.password)
    config_login.navigate_to_configuration("Configuration")
    config_page.wait_for_timeout(2000)

    # Get table info and name from API
    table_info = base_test.Configuration_API.get_table_info(base_test.tableIP)
    table_name = table_info.get("tableName")
    print(f"Table Name: {table_name}")

    # Search for table path in UI and split it
    table_path = config_actions.table_path_search(table_name)
    split_path = config_actions.split_table_path(table_path)
    print(f"Table Path: {table_path}")
    print(f"Split Table Path: {split_path}")

    setup.pause()
