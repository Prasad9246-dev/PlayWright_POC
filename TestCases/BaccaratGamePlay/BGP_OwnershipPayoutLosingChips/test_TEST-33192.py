from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when TIE wins")
def test_TEST_33192(setup):
    TEST_CASE_ID = "TEST-33192"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Fail"
    remarks = ""
    try:
        chips_df = tbd.chips_df
        table_ip = tbd.config.get("tableIP")
        tbd.logger_utils.log(f"Table IP: {table_ip}")
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        tbd.logger_utils.log(f"Buy-in result: {buyin_result}")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        tbd.logger_utils.log(f"Wager result: {wager_result}")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.logger_utils.log("Cards drawn and shoe pressed.")
        tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
        chips_data = tbd.chip_details.extract_chip_details_table()
        tbd.logger_utils.log(f"Extracted chip details: {chips_data}")
        chip_ownership_check = tbd.table_actions.chipOwnership_check(chips_data, ["6001"])
        tbd.logger_utils.log(f"Chip ownership check result: {chip_ownership_check}")
        
        if chip_ownership_check:
            msg = "Ownership verification passed: All chips are owned by player 6001."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            assert True, msg
        else:
            msg = "Ownership verification failed: Not all chips are owned by player 6001."
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