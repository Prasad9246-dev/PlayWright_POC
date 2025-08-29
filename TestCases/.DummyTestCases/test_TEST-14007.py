import time
from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Player antenna logic on commission table")
@allure.story("Insurance on Banker antenna disables Player antenna")
@allure.title("Player antenna should remain off when Banker antenna has insurance on commission table")
def test_TEST_14007(setup):
    TEST_CASE_ID = "TEST-14007"
    FEATURE_NAME = "PlayWright_POC"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Pass"
    remarks = ""
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df

        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        previousGameID = tbd.games_tab.get_first_row_first_column_text()

        buyin_data = tbd.buyin_data
        buyin_data_result = tbd.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
        wager_data = tbd.wager_data
        wager_data_result = tbd.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.ui_utils.click_to_element(tbd.view_table_tab.reveal_button)
        time.sleep(3)
        chips_ID = ",".join(tbd.table_actions.get_chip_ids_for_denom(chips_df, "1000"))
        print(f"Chips ID: {chips_ID}")
        tbd.table_actions.move_chips_between_antennas(table_ip, "TT", "P3", chips_ID)
        tbd.card_processor.deal_cards_and_activate_shoe(table_ip, "2H")
        takebets_list = tbd.take_bets_data
        tbd.take_bets_processor.take(table_ip, wager_data_result, takebets_list)
        tbd.table_actions.move_chips_between_antennas(table_ip, "P3", "TT", chips_ID)
        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        CurrentGameID = tbd.games_tab.get_first_row_first_column_text()

        if previousGameID == CurrentGameID:
            print("Game record is not present on Games tab.")
            tbd.screenshot_util.attach_screenshot(name="Game record is not present on Games tab.")
            tbd.screenshot_util.attach_text("Game record is not present on Games tab.", name="Verification Message")
            status = "Fail"
            remarks = "Game record is not present on Games tab."
            assert previousGameID == CurrentGameID, "Game record is not present on Games tab."
        else:
            print("Game record is present on Games tab.")
            tbd.screenshot_util.attach_screenshot(name="Game record is present on Games tab.")
            tbd.screenshot_util.attach_text("Game record is present on Games tab.", name="Verification Message")
            status = "Pass"
            remarks = "Game record is present on Games tab."
            assert previousGameID != CurrentGameID, "Game record should be present on Games tab."
    except Exception as e:
        status = "Fail"
        remarks = str(e)
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        config = tbd.config
        BUILD_VERSION = config.get("build_version")
        report_writer = TestReportWriter(BUILD_VERSION, FEATURE_NAME)
        report_writer.add_result(
            test_set_name=FEATURE_NAME,
            test_case_id=TEST_CASE_ID,
            status=status,
            remarks=remarks,
            time_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        report_writer.write_report()