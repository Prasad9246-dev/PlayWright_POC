from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when tagged bet is placed on shared antenna")
def test_TEST_33196(setup):
    TEST_CASE_ID = "TEST-33196"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Fail"
    remarks = ""
    chips_df = tbd.chips_df
    table_ip = tbd.config.get("tableIP")
    try:
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        tbd.logger_utils.log(f"Buy-in result: {buyin_result}")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        tbd.logger_utils.log(f"Wager result: {wager_result}")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.logger_utils.log("Cards drawn and shoe pressed.")
        take_result = tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        chips_str = ",".join(take_result[0].get("chips_IDs", []))
        print(chips_str)
        tbd.payout_processor.payout_chips_to_antenna(chips_str, table_ip, "P2")
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
        tbd.configuration_api.update_game_template(tbd.config.get("pp_application_url"), table_ip, [("com.wdts.resolve.game.with.pay.errors", "false")])
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