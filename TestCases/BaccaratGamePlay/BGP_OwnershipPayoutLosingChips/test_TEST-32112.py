from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when resolve game with pay errors is set to YES")
def test_TEST_32112(setup):
    TEST_CASE_ID = "TEST-32112"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Fail"
    remarks = ""
    chips_df = tbd.chips_df
    table_ip = tbd.config.get("tableIP")
    try:
        tbd.configuration_api.update_game_template(tbd.config.get("pp_application_url"), table_ip, [("com.wdts.resolve.game.with.pay.errors", "true")])
        tbd.table_actions.table_close_and_open()
        tbd.table_actions.navigate_to_tab(tbd.view_table_tab.view_table_tab_selector)

        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        tbd.logger_utils.log(f"Buy-in result: {buyin_result}")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        tbd.logger_utils.log(f"Wager result: {wager_result}")
        print(wager_result)
        b1_chips_str = ",".join(
            chip_id
            for entry in wager_result
            if entry.get("antenna") == "B1"
            for chip_id in entry.get("chips_ID", [])
        )
        print(b1_chips_str)
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        tbd.logger_utils.log("Cards drawn and shoe pressed.")
        take_result = tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        chips_str = ",".join(take_result[0].get("chips_IDs", []))
        tbd.payout_processor.payout_chips_to_antenna(chips_str, table_ip, "B1")
        chips = f"{chips_str},{b1_chips_str}" if b1_chips_str else chips_str
        print(chips)
        tbd.table_actions.chip_move_antenna(table_ip, "B1", chips, "false")
        time.sleep(10)
        tbd.table_actions.chip_move_antenna(table_ip, "P1", chips, "true")
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
        tbd.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )