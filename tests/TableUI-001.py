from base_tests.TBDBaseTest import TBDBaseTest
import allure

@allure.feature("Table UI Feature")
@allure.story("Table UI Navigation")
@allure.title("Table UI Navigation Test")
def test_table_ui_navigation(setup, request):
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TableUI")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df

    # Navigate to Games tab
    tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
