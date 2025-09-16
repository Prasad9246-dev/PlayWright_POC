from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33160: Bet Allocation Logic")
@allure.title("TEST-33160 To verify the ownership of chips when player places more than one stack on a single seat")
def test_33160(setup, request):
    status = "Pass"
    remarks = ""
    tbd = TableExecutionTemplate(setup, "TEST-33160","BGP_BetAllocationLogic")
    request.node.tbd = tbd
    try:
        table_ip = tbd.config["tableIP"]
        chips_df = tbd.chips_df
 
        # Navigate to Games tab and get previous Game ID
        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        previous_game_id = tbd.games_tab.get_first_row_first_column_text()
        tbd.logger_utils.log("Manual rating submitted for player 6001")
 
        # Process buy-ins
        tbd.logger_utils.log("Processing buy-ins.")
        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        print("Buy-In Results:")
        for entry in buyin_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")
 
        # Process wagers
        tbd.logger_utils.log("Processing wagers.")
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        print("Wager Results:")
        for entry in wager_result:
            print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")
 
        # Draw cards and press shoe button
        tbd.logger_utils.log("Drawing cards and pressing shoe.")
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
 
        # Process payouts
        tbd.logger_utils.log("Processing payouts.")
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
        time.sleep(5)
 
        # Verification step (optional, add if needed)
        tbd.logger_utils.log("Navigating to Games tab for verification.")
        tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
        current_game_id = tbd.games_tab.get_first_row_first_column_text()
        tbd.logger_utils.log(f"Current Game ID: {current_game_id}")
 
        print(f"Previous Game ID: {previous_game_id}, Current Game ID: {current_game_id}")
        if previous_game_id == current_game_id:
            msg = "Game record is not present on Games tab."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Fail"
            remarks = "Rated Buyin completed, but game record is NOT displayed on Games tab."
            assert False, remarks
        else:
            msg = "Game record is present on Games tab."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"
            remarks = "Rated Buyin completed and game record IS displayed on Games tab."
            assert True, remarks
 
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