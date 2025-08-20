from base_tests.TBDBaseTest import TBDBaseTest
import allure

@allure.feature("Buy-In Feature")
@allure.story("TEST-0608: Rated Buy-In")
@allure.title("TEST-0608 Rated Buy-In Test")
def test_0608(setup,request):
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TEST-0608")
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

    # Take bets
    tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)

    # Verify game ID increment logic
    tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
    current_game_id = tbd.games_tab.get_first_row_first_column_text()

    # Assertion and reporting
    print(f"Previous Game ID: {previous_game_id}, Current Game ID: {current_game_id}")
    if previous_game_id == current_game_id:
        msg = "Game record is not present on Games tab."
        print(msg)
        tbd.screenshot_util.attach_screenshot(name=msg)
        tbd.screenshot_util.attach_text(msg, name="Verification Message")
        assert False, "Rated Buyin completed, but game record is NOT displayed on Games tab."
    else:
        msg = "Game record is present on Games tab."
        print(msg)
        tbd.screenshot_util.attach_screenshot(name=msg)
        tbd.screenshot_util.attach_text(msg, name="Verification Message")
        assert True, "Rated Buyin completed and game record IS displayed on Games tab."