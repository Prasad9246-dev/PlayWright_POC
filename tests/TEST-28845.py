import time
from tests.BaseTest import BaseTest
import allure

@allure.feature("Take messaging visibility on the screen")
@allure.story("Verify 'TAKE PLAYER' element appears after buy-in and wager")
@allure.title("'TAKE PLAYER' element should be visible after buy-in and wager")
def test_run_TEST_28845(setup,request):
    base_test = BaseTest(setup,"TEST-28845")
    request.node.base_test = base_test
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df
    
    # Get buy-in data from Excel for this test case
    buyin_data = base_test.buyin_data
    buyin_data_result = base_test.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    # Process wagers after buy-in
    wager_data = base_test.wager_data
    wager_data_result = base_test.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
    # Draw cards and press shoe button
    base_test.card_processor.draw_cards_and_shoe_press(base_test.card_data, table_ip)    
    
    time.sleep(5)  # Wait for the cards to be drawn
    is_visible = base_test.view_table_tab.is_take_player_visible()  
    if is_visible:
        print("TAKE PLAYER element is visible on the screen")
        base_test.screenshot_util.attach_screenshot(name="TAKE PLAYER Visible - Pass")
        base_test.screenshot_util.attach_text("TAKE PLAYER element is visible on the screen", name="Verification Message")
        assert is_visible, "'TAKE PLAYER' element should be visible on the screen"
    else:
        print("TAKE PLAYER element is not visible on the screen")
        base_test.screenshot_util.attach_screenshot(name="TAKE PLAYER Not Visible - Fail")
        base_test.screenshot_util.attach_text("TAKE PLAYER element is NOT visible on the screen", name="Verification Message")
        assert is_visible, "'TAKE PLAYER' element is not visible on the screen"
            
    # Take bets using the wager results
    takebets_list = base_test.take_bets_data
    base_test.take_bets_processor.take(table_ip, wager_data_result, takebets_list)