from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure

@allure.feature("Baccarat Game Play")
@allure.story("Game play-ownership after paying out from losing chips")
@allure.title("To verify the ownership of chips when player verification is ON")
def test_TEST_32113(setup):
    TEST_CASE_ID = "TEST-32113"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Fail"
    remarks = ""
    try:
        chips_df = tbd.chips_df
        table_ip = tbd.config.get("tableIP")
        tbd.logger_utils.log(f"Table IP: {table_ip}")
        tbd.configuration_api.update_template([("com.wdts.bt.require.player.verification","true")], tbd.config.get("pp_application_url"), table_ip, "BUSINESS_RULES")
        tbd.table_actions.table_close_and_open()
        tbd.table_actions.navigate_to_tab(tbd.view_table_tab.view_table_tab_selector)

        li_chips = tbd.table_actions.get_chip_ids_for_denom(chips_df, "1000")
        chips_str = ','.join(li_chips)
        tbd.table_actions.move_chips_between_antennas(table_ip, "TT", "P1", chips_str)

        buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
        
        wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
        
        tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
        
        tbd.take_bets_processor.take(table_ip, wager_result, tbd.take_bets_data)
        
        tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
        
        chips_data = tbd.chip_details.extract_chip_details_table()
        tbd.logger_utils.log(f"Extracted chip details: {chips_data}")
        chip_ownership_check = tbd.table_actions.is_owner_only_anonymous(chips_data)
        tbd.logger_utils.log(f"Chip ownership check result: {chip_ownership_check}")
    
        if chip_ownership_check:
            msg = "Ownership verification passed: All chips ownership is Anonymous."
            print(msg)
            tbd.logger_utils.log(msg)
            tbd.screenshot_util.attach_screenshot(name=msg)
            tbd.screenshot_util.attach_text(msg, name="Verification Message")
            status = "Pass"  
            assert True, msg
        else:
            msg = "Ownership verification failed: Not all chips ownership is Anonymous."
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
        tbd.configuration_api.update_template([("com.wdts.bt.require.player.verification","false")], tbd.config.get("pp_application_url"), table_ip, "BUSINESS_RULES")
        tbd.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )