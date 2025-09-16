from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33163: Bet Allocation Logic")
@allure.title("TEST-33163 To verify bet attribution when anonymous player places bet on Rated position")
def test_33163(setup, request):
    status = "Pass"
    remarks = ""
    tbd = TableExecutionTemplate(setup, "TEST-33163","BGP_BetAllocationLogic")
    request.node.tbd = tbd
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df
        #Player clocked-in
        tbd.table_actions.clock_in_player("Players_TAB","1", "6013")
        time.sleep(2)
        tbd.table_actions.navigate_to_tab(tbd.view_table_tab.view_table_tab_selector)
        chip_id = tbd.table_actions.get_chip_ids_for_denom(chips_df,100)
        # # Process buy-ins
        # tbd.logger_utils.log("Processing buy-ins.")
        # chip_id = tbd.table_actions.get_chip_ids_for_denom(chips_df,100)

        # Convert chip_id list to string
        chip_id_str = ",".join(str(x) for x in chip_id)

        # Process wagers
        tbd.logger_utils.log("Processing wagers.")
        tbd.table_actions.move_chips_between_antennas(table_ip, "TT", "P1", chip_id_str)

        # Draw cards and press shoe button
        tbd.logger_utils.log("Drawing cards and pressing shoe.")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
 
        # Process payouts
        tbd.logger_utils.log("Processing payouts.")
        chip_id = tbd.table_actions.get_chip_ids_for_denom(chips_df,100)

        # Convert chip_id list to string
        chip_id_str = ",".join(str(x) for x in chip_id)

        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
        time.sleep(5)

        tbd.table_actions.move_chips_between_antennas(table_ip, "TT", "P1", chip_id_str)
    
        # After payout code
        tbd.logger_utils.log("Navigating to Sessions tab.")
        setup.get_by_role("tab", name="Sessions").click()
        tbd.logger_utils.log("Clicked Sessions tab.")

        tbd.logger_utils.log("Checking for any cell containing 'Anonymous'.")
        anonymous_cells = setup.locator("[role='cell']")
        found_anonymous = False
        for i in range(anonymous_cells.count()):
            cell_text = anonymous_cells.nth(i).inner_text().strip()
            if "Anonymous" in cell_text:
                found_anonymous = True
                break
        if found_anonymous:
            print("Anonymous is available on screen: successful assertion")
            tbd.logger_utils.log("Anonymous is available on screen: successful assertion")
            assert True, "Anonymous is available on screen: successful assertion"
        else:
            print("Anonymous is not available on screen: failed assertion")
            tbd.logger_utils.log("Anonymous is not available on screen: failed assertion")
            assert False, "Anonymous is not available on screen: failed assertion"

        tbd.logger_utils.log("Navigating to Players tab.")
        setup.get_by_role("tab", name="Players").click()
        tbd.logger_utils.log("Clicked Players tab.")
    
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