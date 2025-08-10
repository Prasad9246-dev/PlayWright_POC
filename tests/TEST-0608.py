from tests.BaseTest import BaseTest
import allure
from utils.excel_reader import get_buyin_data
from GameSkeleton.BuyIN import BuyIN

@allure.feature("Buy-In Feature")
@allure.story("TEST-0608: Rated Buy-In")
@allure.title("TEST-0608 Rated Buy-In Test")
def test_run_TEST_0608(setup):
    base_test = BaseTest(setup,"TEST-0608")
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df
    # Get buy-in data from Excel for this test case
    buyin_data = base_test.buyin_data
    result = base_test.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    print("Buy-In Results:")
    for entry in result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}") 
    
    # Process wagers after buy-in
    wager_data = base_test.wager_data
    wager_data_result = base_test.wager_processor.process_wagers(table_ip, result, wager_data)
    print("Wager Results:")
    for entry in wager_data_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")

    # Draw cards and press shoe button
    base_test.card_processor.draw_cards_and_shoe_press(base_test.card_data, table_ip)
    
    # Take bets using the wager results
    takebets_list = base_test.take_bets_data
    base_test.take_bets_processor.take(table_ip, wager_data_result, takebets_list)
    
    # Process payouts
    payout_data = base_test.payout_data
    base_test.payout_processor.process_payouts(table_ip, payout_data, base_test.chips_df)