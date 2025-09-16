from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33165: Bet Allocation Logic")
@allure.title("TEST-33165 This test case is to verify the bet attribution when known player places bet on position where anonymous session is already created.")
def test_33165(setup, request):
    status = "Pass"
    remarks = ""
    tbd = TableExecutionTemplate(setup, "TEST-33165","BGP_BetAllocationLogic")
    request.node.tbd = tbd
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df
              
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
        tbd.table_actions.move_chips_between_antennas(table_ip, "P1", "TT", chip_id_str)

        # Process buy-ins - Game 2 Known Session
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
        tbd.take_bets_processor.take(table_ip,wager_result,tbd.take_bets_data)
        time.sleep(5)
 
        # Move to players tab for verification
        tbd.logger_utils.log("Navigating to Players tab for verification.")
        tbd.table_actions.navigate_to_tab(tbd.player_tab.Players_TAB)
        # Verification of Player Tab Card
        tbd.logger_utils.log("Verifying if player link (6001) is visible on Player Tab Card.")
        player_link = setup.get_by_role("link", name="(6001)")
        if player_link.is_visible():
            print("Player link (6001) is visible and clicked: successful assertion")
            tbd.logger_utils.log("Player link (6001) is visible and clicked: successful assertion")
            assert True, "Player link (6001) is visible and clickable: successful assertion"
        else:
            print("Player link (6001) is not visible: failed assertion")
            tbd.logger_utils.log("Player link (6001) is not visible: failed assertion")
            assert False, "Player link (6001) is not visible: failed assertion"
    
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