from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase1: Rated Buy-In")
@allure.title("test_DummyTestCase1 Rated Buy-In Test")
def test_TEST_0608(setup):
    tbd = TableExecutionTemplate(setup, "TEST-0608","PlayWright_POC")
    status = "Pass"
    remarks = ""
    try:
        # Your test logic here
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df

        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        previous_game_id = tbd.games_tab.get_first_row_first_column_text()

        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        print("Buy-In Results:")
        for entry in buyin_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")

        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        print("Wager Results:")
        for entry in wager_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")

        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)

        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        current_game_id = tbd.games_tab.get_first_row_first_column_text()

        print(f"Previous Game ID: {previous_game_id}, Current Game ID: {current_game_id}")
        if previous_game_id == current_game_id:
            msg = "Game record is not present on Games tab."
            print(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Fail"
            remarks = "Rated Buyin completed, but game record is NOT displayed on Games tab."
            assert False, remarks
        else:
            msg = "Game record is present on Games tab."
            print(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            remarks = "Rated Buyin completed and game record IS displayed on Games tab."
            assert True, remarks

    except Exception as e:
        status = "Fail"
        remarks = str(e)
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        # Custom report writing
        
        # config_utils = ConfigUtils()
        config = tbd.config
        BUILD_VERSION = config.get("build_version")
        # FEATURE_NAME = config_utils.set_feature_name(tbd.feature_name)
        FEATURE_NAME = config.get("feature_name")
        report_writer = TestReportWriter(BUILD_VERSION, FEATURE_NAME)
        report_writer.add_result(
            test_set_name=FEATURE_NAME,
            test_case_id="TEST-0608",
            status=status,
            remarks=remarks,
            time_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        report_writer.write_report()