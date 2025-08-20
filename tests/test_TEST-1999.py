from base_tests.TBDBaseTest import TBDBaseTest
import allure
from pages.ConfigurationLoginPage import ConfigurationLoginPage
from utils.ConfigurationActions import ConfigurationActions
from pages.ConfigurationPage import ConfigurationPage
from utils.UIUtils import UIUtils
from pages.CasinoManager import CasinoManager


@allure.feature("Buy-In Feature")
@allure.story("TEST-1999: Rated Buy-In")
@allure.title("TEST-1999 Rated Buy-In Test")
def test_1999(setup,request):
    # Initialize base test and page objects
    tbd = TBDBaseTest(setup, "TEST-1999")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    username = tbd.config["username"]
    password = tbd.config["password"]
    config_page = setup.context.new_page()
    config_page.goto(tbd.config["base_url"])

    # Login to configuration
    config_login = ConfigurationLoginPage(config_page)
    config_actions = ConfigurationActions(config_page)
    configuration_page = ConfigurationPage(config_page)
    ui_Utils = UIUtils(config_page)
    config_login.configuration_login(username, password)
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
    casino_manager.manual_ratings_tab.click()
    ui_Utils.click_to_element(page1.get_by_role("heading", name="No data available"))

