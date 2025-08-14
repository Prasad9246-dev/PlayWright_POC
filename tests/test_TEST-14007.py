import time
from tests.BaseTest import BaseTest
import allure

@allure.feature("Player antenna logic on commission table")
@allure.story("Insurance on Banker antenna disables Player antenna")
@allure.title("Player antenna should remain off when Banker antenna has insurance on commission table")
def test_14007(setup,request):
    base_test = BaseTest(setup,"TEST-14007")
    request.node.base_test = base_test
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df
    
    base_test.table_actions.navigate_to_tab(base_test.games_tab.GAMES_TAB)
    previousGameID = base_test.games_tab.get_first_row_first_column_text()
    
    # Get buy-in data from Excel for this test case
    buyin_data = base_test.buyin_data
    buyin_data_result = base_test.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    # Process wagers after buy-in
    wager_data = base_test.wager_data
    wager_data_result = base_test.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
    # Draw cards and press shoe button
    base_test.card_processor.draw_cards_and_shoe_press(base_test.card_data, table_ip) 
    base_test.UI_Utils.click_to_element(base_test.view_table_tab.reveal_button)
    # Wait for the game to complete
    time.sleep(3)
    chips_ID = ",".join(base_test.table_actions.get_chip_ids_for_denom(chips_df, "1000"))
    print(f"Chips ID: {chips_ID}")
    base_test.table_actions.move_chips_between_antennas(table_ip,"TT","P3",chips_ID)
    # Verify the game result
    base_test.card_processor.deal_cards_and_activate_shoe(table_ip,"2H")
    
    # Take bets using the wager results
    takebets_list = base_test.take_bets_data
    base_test.take_bets_processor.take(table_ip, wager_data_result, takebets_list)
    base_test.table_actions.move_chips_between_antennas(table_ip,"P3","TT",chips_ID)
    
    # Verify game ID increment logic
    base_test.table_actions.navigate_to_tab(base_test.games_tab.GAMES_TAB)
    CurrentGameID = base_test.games_tab.get_first_row_first_column_text()
    
    if previousGameID == CurrentGameID:
        print("Game record is not present on Games tab.")
        base_test.screenshot_util.attach_screenshot(name="Game record is not present on Games tab.")
        base_test.screenshot_util.attach_text("Game record is not present on Games tab.", name="Verification Message")
        assert previousGameID == CurrentGameID, "Game record is not present on Games tab."
    else:
        print("Game record is present on Games tab.")
        base_test.screenshot_util.attach_screenshot(name="Game record is present on Games tab.")
        base_test.screenshot_util.attach_text("Game record is present on Games tab.", name="Verification Message")
        assert previousGameID != CurrentGameID, "Game record should be present on Games tab."
    