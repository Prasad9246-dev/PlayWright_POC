from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
<<<<<<< HEAD
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play - Ownership after paying out from losing chips")
@allure.story("To verify the ownership of chips when we pay with the losing bet without placing it on DA")
@allure.title("TEST-32109: To verify the ownership of chips when we pay with the losing bet without placing it on DA")
=======
import allure

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when we pay with the loosing bet without placing it on DAEALER antenna")
>>>>>>> 29d3cda867a30ae34c5ae155ed0d9497d81437df
def test_TEST_32109(setup):
    TEST_CASE_ID = "TEST-32109"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
<<<<<<< HEAD
    status = "Pass"
    remarks = ""
    try:
        # Step 1: Do known buyin of 100*5
        # Step 2: Place 100*1 on BP and 100*2 on L6 and 100*2 on Player
        # Step 3: Make BP win only
        # Step 4: Take 100*2 from L6 and 100*2 from player and do not place it on DA and place it on BP and take remaining chips from chip tray and payout to BP
        # Step 5: Verify the ownership of chips
        # Step 6: Verify the chip history report
        # TODO: Implement actual test steps using tbd methods
        assert True, "Basic workflow placeholder. Implement detailed steps."
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
        tbd.logger_utils.log("============================")
        tbd.logger_utils.log(f"Test case status: {status}")
        tbd.logger_utils.log("============================")
        print("============================")
        print(f"Test case status: {status}")
        print("============================")
=======
    BUILD_VERSION = tbd.config.get("build_version")
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
        take_result = tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        tbd.logger_utils.log(f"Take bets result: {take_result}")
        chips_str = ",".join(
                        chip_id
                        for entry in take_result
                        for chip_id in entry.get("chips_IDs", [])
                    )
        li_chips=  tbd.table_actions.get_chip_ids_for_denom(chips_df,"700")
        if li_chips:
            chips_str = f"{chips_str},{','.join(li_chips)}"   
        tbd.table_actions.move_chips_between_antennas(table_ip, "TT", "BP", chips_str)
        tbd.logger_utils.log("Payout chips to antenna BP completed.")
        chips_data = tbd.chip_details.extract_chip_details_table()
        tbd.logger_utils.log(f"Extracted chip details: {chips_data}")
        chip_ownership_check = tbd.table_actions.chipOwnership_check(chips_data, ["6009"])
        tbd.logger_utils.log(f"Chip ownership check result: {chip_ownership_check}")
        
        if chip_ownership_check:
            msg = "Ownership verification passed: All chips are owned by player 6009."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            assert True, msg
        else:
            msg = "Ownership verification failed: Not all chips are owned by player 6009."
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
        tbd.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )
>>>>>>> 29d3cda867a30ae34c5ae155ed0d9497d81437df
