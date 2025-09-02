from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure
from playwright.sync_api import Page
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33160: Bet Allocation Logic")
@allure.title("TEST-33160 To verify the ownership of chips when player places more than one stack on a single seat")
def test_33160(setup,request):
    # Initialize base test and get required data
    tbd = TableExecutionTemplate(setup, "TEST-33160")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df
 
    # Navigate to Games tab and get previous Game ID
    tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
    previous_game_id = tbd.games_tab.get_first_row_first_column_text()
 
    # Process buy-ins
    buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
    print("Buy-In Results:")
    for entry in buyin_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")
 
    # Process wagers
    wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
    print("Wager Results:")
    for entry in wager_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")
 
    # Draw cards and press shoe button
    tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
 
    # Process payouts
    tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
    time.sleep(5)
