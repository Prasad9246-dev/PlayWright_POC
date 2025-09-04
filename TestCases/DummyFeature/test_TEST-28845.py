import time
from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Take messaging visibility on the screen")
@allure.story("Verify 'TAKE PLAYER' element appears after buy-in and wager")
@allure.title("'TAKE PLAYER' element should be visible after buy-in and wager")
def test_TEST_28845(setup):
    TEST_CASE_ID = "TEST-28845"
    FEATURE_NAME = "DummyFeature"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Pass"
    remarks = ""
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df

        buyin_data = tbd.buyin_data
        buyin_data_result = tbd.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
        wager_data = tbd.wager_data
        wager_data_result = tbd.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)

        time.sleep(5)  # Wait for the cards to be drawn
        is_visible = tbd.view_table_tab.is_take_player_visible()
        if is_visible:
            print("TAKE PLAYER element is visible on the screen")
            tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Visible - Pass")
            tbd.screenshot_util.attach_text("TAKE PLAYER element is visible on the screen", name="Verification Message")
            status = "Pass"
            remarks = "'TAKE PLAYER' element is visible on the screen"
            assert is_visible, "'TAKE PLAYER' element should be visible on the screen"
        else:
            print("TAKE PLAYER element is not visible on the screen")
            tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Not Visible - Fail")
            tbd.screenshot_util.attach_text("TAKE PLAYER element is NOT visible on the screen", name="Verification Message")
            status = "Fail"
            remarks = "'TAKE PLAYER' element is not visible on the screen"
            assert is_visible, "'TAKE PLAYER' element is not visible on the screen"

        takebets_list = tbd.take_bets_data
        tbd.take_bets_processor.take(table_ip, wager_data_result, takebets_list)
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