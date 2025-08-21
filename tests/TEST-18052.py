from tests.BaseTest import BaseTest
from utils.excel_reader import get_buyin_data
from GameSkeleton.BuyIN import BuyIN
import time

def test_run_TEST_18052(setup):
    base_test = BaseTest(setup, "TEST-18052")
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df

    # Prepare buy-in data for $25 * 1
    buyin_data = base_test.buyin_data
    buyin_result = base_test.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    print("Buy-In Results:")
    for entry in buyin_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")
    
    wager_data = base_test.wager_data
    wager_result = base_test.wager_processor.process_wagers(table_ip, buyin_result, wager_data)
    print("Wager Results:")
    for entry in wager_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")

    base_test.card_processor.draw_cards_and_shoe_press(base_test.card_data, table_ip)
    payout_data = base_test.payout_data
    base_test.payout_processor.process_payouts(table_ip, payout_data, chips_df)

    # Optionally, add assertions to verify buy-in
    # Call change_transaction_from_view_table
    time.sleep(2)
    base_test.table_actions.change_transaction_from_view_table(table_ip, chips_df)

    base_test.table_actions.navigate_to_tab(base_test.Player_Tab.PLAYERS_TAB)
    # Move to Session tab
    base_test.table_actions.table_close_and_open()
    # base_test.table_actions.move_to_sessions_tab()
    base_test.table_actions.check_chip_in_value(expected_value="25")