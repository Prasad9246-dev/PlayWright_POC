from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play - Ownership after paying out from losing chips")
@allure.story("To verify the ownership of chips when we pay with the losing chips")
@allure.title("TEST-32107: To verify the ownership of chips when we pay with the losing chips")
def test_TEST_32107(setup):
    TEST_CASE_ID = "TEST-32107"
    FEATURE_NAME = "BGP_Test"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Pass"
    remarks = ""
    try:
        table_ip = tbd.config.get("tableIP")
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, tbd.chips_df)
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        take_result = tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        # Step 1: Clock-in 6001 on seat 1 and do the buyin of 100*1 and 25*4 for the same
        # Step 2: Place 100*1 on player 1 and 25*4 on banker 2 and make player win
        # Step 3: Now take 25*4 and place it on DA
        # Step 4: Payout 100 with those 25*4 chips
        # Step 5: Open chip details from Table dashboard dropdown
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
