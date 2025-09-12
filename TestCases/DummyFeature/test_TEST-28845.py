import time
from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure

@allure.feature("Take messaging visibility on the screen")
@allure.story("test_DummyTestCase4: TAKE PLAYER visibility test")
@allure.title("test_DummyTestCase4: TAKE PLAYER visibility test")
def test_TEST_28845(setup):
    TEST_CASE_ID = "TEST-28845"
    FEATURE_NAME = "DummyFeature"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Fail"
    remarks = ""
    try:
        tbd.logger_utils.log("Starting test_TEST_28845: TAKE PLAYER visibility test")
        table_ip = tbd.config.get("tableIP")
        chips_df = tbd.chips_df

        tbd.logger_utils.log("Processing buy-ins.")
        buyin_data = tbd.buyin_data
        buyin_data_result = tbd.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
        tbd.logger_utils.log(f"Buy-In Results: {buyin_data_result}")

        tbd.logger_utils.log("Processing wagers.")
        wager_data = tbd.wager_data
        wager_data_result = tbd.wager_processor.process_wagers(table_ip, buyin_data_result, wager_data)
        tbd.logger_utils.log(f"Wager Results: {wager_data_result}")

        tbd.logger_utils.log("Drawing cards and pressing shoe.")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)

        tbd.logger_utils.log("Waiting for cards to be drawn.")
        time.sleep(5)

        tbd.logger_utils.log("Checking if TAKE PLAYER element is visible.")
        is_visible = tbd.view_table_tab.is_take_player_visible()
        if is_visible:
            msg = "TAKE PLAYER element is visible on the screen"
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Visible - Pass")
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            remarks = "'TAKE PLAYER' element is visible on the screen"
            assert is_visible, "'TAKE PLAYER' element should be visible on the screen"
        else:
            msg = "TAKE PLAYER element is not visible on the screen"
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name="TAKE PLAYER Not Visible - Fail")
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            remarks = "'TAKE PLAYER' element is not visible on the screen"
            assert is_visible, "'TAKE PLAYER' element is not visible on the screen"

        tbd.logger_utils.log("Processing take bets.")
        takebets_list = tbd.take_bets_data
        tbd.take_bets_processor.take(table_ip, wager_data_result, takebets_list)
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
        