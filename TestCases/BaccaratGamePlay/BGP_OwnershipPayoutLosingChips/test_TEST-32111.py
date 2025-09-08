from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when we do overpay")
def test_TEST_32111(setup):
    TEST_CASE_ID = "TEST-32111"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Fail"
    remarks = ""
    try:
        chips_df = tbd.chips_df
        table_ip = tbd.config.get("tableIP")
        tbd.configuration_api.update_template([("com.wdts.table.single.press.auto.settle.via.shoe", "true")],tbd.config.get("pp_application_url"),table_ip, "TABLE")
        tbd.table_actions.table_close_and_open()
        tbd.table_actions.navigate_to_tab(tbd.view_table_tab.view_table_tab_selector)

        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        tbd.logger_utils.log(f"Buy-in result: {buyin_result}")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        tbd.logger_utils.log(f"Wager result: {wager_result}")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.logger_utils.log("Cards drawn and shoe pressed.")
        take_result = tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        chips_str = ",".join(take_result[0].get("chips_IDs", []))
        tbd.payout_processor.payout_chips_to_antenna(chips_str, table_ip, "P1")
        time.sleep(2)
        tbd.card_processor.press_shoe_button(table_ip)
        chips_data = tbd.chip_details.extract_chip_details_table()
        tbd.logger_utils.log(f"Extracted chip details: {chips_data}")
        chip_ownership_check = tbd.table_actions.is_owner_only_anonymous(chips_data)
        tbd.logger_utils.log(f"Chip ownership check result: {chip_ownership_check}")
    
        if chip_ownership_check:
            msg = "Ownership verification passed: All chips ownership is Anonymous."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"  
            assert True, msg
        else:
            msg = "Ownership verification failed: Not all chips ownership is Anonymous."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            assert False, msg

    except Exception as e:
        remarks = str(e)
        tbd.logger_utils.log(f"Exception occurred: {remarks}")
        try:
            tbd.void_game()
            tbd.logger_utils.log("Game voided due to exception.")
        except Exception as ve:
            tbd.logger_utils.log(f"Failed to void hand in test: {ve}")
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
        tbd.logger_utils.log("========================================================")
        tbd.logger_utils.log(f"Test result written: {status}")
        tbd.logger_utils.log("========================================================")
        print(f"Test case status: {status}")