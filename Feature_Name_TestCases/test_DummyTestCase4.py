import time
from Execution_Templates.Table_Execution_Template import TableExecutionTemplate
import allure

@allure.feature("Take messaging visibility on the screen")
@allure.story("Verify 'TAKE PLAYER' element appears after buy-in and wager")
@allure.title("'TAKE PLAYER' element should be visible after buy-in and wager")
def test_DummyTestCase4(setup,request):
    tbd = TableExecutionTemplate(setup,"TEST-28845")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df

    # Get buy-in data from Excel for this test case
    buyin_data = tbd.buyin_data
    buyin_data_result = tbd.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    # Process wagers after buy-in
    wager_data = tbd.wager_data
    wager_data_result = tbd.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
    # Draw cards and press shoe button
    tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)

    time.sleep(5)  # Wait for the cards to be drawn
    is_visible = tbd.view_table_tab.is_take_player_visible()
    if is_visible:
        print("TAKE PLAYER element is visible on the screen")
        tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Visible - Pass")
        tbd.screenshot_util.attach_text("TAKE PLAYER element is visible on the screen", name="Verification Message")
        assert is_visible, "'TAKE PLAYER' element should be visible on the screen"
    else:
        print("TAKE PLAYER element is not visible on the screen")
        tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Not Visible - Fail")
        tbd.screenshot_util.attach_text("TAKE PLAYER element is NOT visible on the screen", name="Verification Message")
        assert is_visible, "'TAKE PLAYER' element is not visible on the screen"
            
    # Take bets using the wager results
    takebets_list = tbd.take_bets_data
    tbd.take_bets_processor.take(table_ip, wager_data_result, takebets_list)