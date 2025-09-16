from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33170: Bet Allocation Logic")
@allure.title("TEST-33170 To verify the bet attribution when player clocked-in one seat and wager bet on shared antenna")
def test_33170(setup, request):
    status = "Pass"
    remarks = ""
    tbd = TableExecutionTemplate(setup, "TEST-33170","BGP_BetAllocationLogic")
    request.node.tbd = tbd
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df

        # Process buy-ins
        tbd.logger_utils.log("Processing buy-ins.")
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)

        # Process wagers
        tbd.logger_utils.log("Processing wagers.")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
 
        # Draw cards and press shoe button
        tbd.logger_utils.log("Drawing cards and pressing shoe.")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
 
        # Process payouts
        tbd.logger_utils.log("Processing payouts.")
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
        time.sleep(5)

        # Move to Games tab for verification
        tbd.logger_utils.log("Navigating to Games tab for verification.")
        tbd.table_actions.navigate_to_tab(tbd.games_tab.games_tab_locator)

        # Step: Click the first row, first column cell in the table
        tbd.logger_utils.log("Clicking the first row, first column cell in the table.")
        first_row_first_column = tbd.games_tab.first_row_first_column
        first_row_first_column.click()
        tbd.logger_utils.log("Clicked the first row, first column cell.")
        time.sleep(8)
        # Step: Extract dynamic table into Python datatable (list of dicts)
        tbd.logger_utils.log("Extracting table data into Python datatable.")
        print("Extracting table data...")
        table_data = tbd.games_tab.extract_nested_details_table_data()
        tbd.logger_utils.log(f"Extracted table data: {table_data}")

        # Validate: Player column contains '6002' and Bets column contains 1500 and 200
        tbd.logger_utils.log("Validating that Player column contains '6002'.")
        found_6002 = False
        for row in table_data:
            player = row.get('Player', '')
            if '6002' in str(player):
                found_6002 = True
                break
        if found_6002:
            msg = "Verification passed: Player column contains '6002'."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            assert True, msg
        else:
            msg = "Verification failed: Player column does not contain '6002'."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Fail"
            assert False, msg

        # Validate: Bet Type column contains 'PP'
        tbd.logger_utils.log("Validating that Bet Type column contains 'PP'.")
        found_pp = False
        for row in table_data:
            bet_type = row.get('Bet Type', '')
            if 'PP' in str(bet_type):
                found_pp = True
                break
        if found_pp:
            msg = "Verification passed: Bet Type column contains 'PP'."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            assert True, msg
        else:
            msg = "Verification failed: Bet Type column does not contain 'PP'."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Fail"
            assert False, msg
    
    except Exception as e:
        status = "Fail"
        remarks = str(e)
        tbd.logger_utils.log(f"Exception occurred: {remarks}")
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
            tbd.logger_utils.log(f"Failed to void hand in test: {ve}")
        raise
    finally:
        config = tbd.config
        BUILD_VERSION = config.get("build_version")
        FEATURE_NAME = config.get("feature_name")
        report_writer = TestReportWriter(BUILD_VERSION, FEATURE_NAME)
        report_writer.add_result(
            test_set_name=FEATURE_NAME,
            test_case_id="TEST-33170",
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