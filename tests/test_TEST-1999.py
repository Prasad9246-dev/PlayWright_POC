from base_tests.TBDBaseTest import TBDBaseTest
import allure


@allure.feature("Buy-In Feature")
@allure.story("TEST-1999: Rated Buy-In")
@allure.title("TEST-1999 Rated Buy-In Test")
def test_1999(setup,request):
    # Initialize base test and page objects
    tbd = TBDBaseTest(setup, "TEST-1999")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    
    tbd.table_actions.navigate_to_tab(tbd.player_tab.Players_TAB)
    tbd.UI_Utils.click_to_element(tbd.player_tab.player_card_position(2))
    tbd.UI_Utils.fill_element(tbd.player_tab.Enter_Player_ID, "6001")
    tbd.UI_Utils.press_enter(tbd.player_tab.Enter_Player_ID)
    tbd.UI_Utils.click_to_element(tbd.player_tab.first_row_first_col_selector)
    tbd.UI_Utils.click_to_element(tbd.player_tab.clock_in_player_button)
    setup.pause()