from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase1: Rated Buy-In")
@allure.title("test_DummyTestCase1 Rated Buy-In Test")
def test_TEST_0608(setup):
    TEST_CASE_ID = "TEST-0608"
    FEATURE_NAME = "DummyFeature"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Fail"
    remarks = ""
    try:
        tbd.logger_utils.log("Starting test_TEST-0608: Rated Buy-In Test")
        table_ip = tbd.config.get("tableIP")
        chips_df = tbd.chips_df

        tbd.logger_utils.log("Navigating to Games tab.")
        tbd.table_actions.navigate_to_tab(tbd.games_tab.games_tab_locator)
        previous_game_id = tbd.games_tab.get_first_row_first_column_text()
        tbd.logger_utils.log(f"Previous Game ID: {previous_game_id}")

        tbd.logger_utils.log("Processing buy-ins.")
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        print("Buy-In Results:")
        for entry in buyin_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")

        tbd.logger_utils.log("Processing wagers.")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        print("Wager Results:")
        for entry in wager_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")

        tbd.logger_utils.log("Drawing cards and pressing shoe.")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)

        tbd.logger_utils.log("Processing payouts.")
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)

        tbd.logger_utils.log("Navigating to Games tab for verification.")
        tbd.table_actions.navigate_to_tab(tbd.games_tab.games_tab_locator)
        current_game_id = tbd.games_tab.get_first_row_first_column_text()
        tbd.logger_utils.log(f"Current Game ID: {current_game_id}")

        print(f"Previous Game ID: {previous_game_id}, Current Game ID: {current_game_id}")
        if previous_game_id == current_game_id:
            msg = "Game record is not present on Games tab."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            remarks = "Rated Buyin completed, but game record is NOT displayed on Games tab."
            assert False, remarks
        else:
            msg = "Game record is present on Games tab."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            remarks = "Rated Buyin completed and game record IS displayed on Games tab."
            assert True, remarks

    except Exception as e:
        remarks = str(e)
        tbd.logger_utils.log(f"Exception occurred: {remarks}")
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
            tbd.logger_utils.log(f"Failed to void hand in test: {ve}")
        raise
    finally:
        tbd.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )