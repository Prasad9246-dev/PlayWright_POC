from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33161: Bet Allocation Logic")
@allure.title("TEST-33161 To verify the bet attribution when multiple rated players is present on a single seat and we paid out as single stack")
def test_33161(setup, request):
    status = "Pass"
    remarks = ""
    tbd = TableExecutionTemplate(setup, "TEST-33161","BGP_BetAllocationLogic")
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
 
        # Verification step (optional, add if needed)
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
        # Step: Validate Position column contains 1
        tbd.logger_utils.log("Validating if Position column contains 1.")
        position_found = any((row.get('Position') or '').strip() == '1' for row in table_data)
        if position_found:
            print("Position column contains 1: successful assertion")
            tbd.logger_utils.log("Position column contains 1: successful assertion")
            assert True, "Position column contains 1: successful assertion"
        else:
            print("Position column does not contain 1: failed assertion")
            tbd.logger_utils.log("Position column does not contain 1: failed assertion")
            assert False, "Position column does not contain 1: failed assertion"

        # Step: Validate Player column contains 6002
        tbd.logger_utils.log("Validating if Player column contains 6002.")
        player_found = any('6002' in (row.get('Player') or '') for row in table_data)
        if player_found:
            print("Player column contains 6002: successful assertion")
            tbd.logger_utils.log("Player column contains 6002: successful assertion")
            assert True, "Player column contains 6002: successful assertion"
        else:
            print("Player column does not contain 6002: failed assertion")
            tbd.logger_utils.log("Player column does not contain 6002: failed assertion")
            assert False, "Player column does not contain 6002: failed assertion"

        # Step: Validate Bets column contains 1500
        tbd.logger_utils.log("Validating if Bets column contains 1500.")
        bets_found = any('1500' in (row.get('Bets') or '').replace(',', '').replace(' ', '') for row in table_data)
        if bets_found:
            print("Bets column contains 1500: successful assertion")
            tbd.logger_utils.log("Bets column contains 1500: successful assertion")
            assert True, "Bets column contains 1500: successful assertion"
        else:
            print("Bets column does not contain 1500: failed assertion")
            tbd.logger_utils.log("Bets column does not contain 1500: failed assertion")
            assert False, "Bets column does not contain 1500: failed assertion"

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
            test_case_id="TEST-0608",
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