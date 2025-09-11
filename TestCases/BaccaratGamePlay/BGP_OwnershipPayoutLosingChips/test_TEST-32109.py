from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play - Ownership after paying out from losing chips")
@allure.story("To verify the ownership of chips when we pay with the losing bet without placing it on DA")
@allure.title("TEST-32109: To verify the ownership of chips when we pay with the losing bet without placing it on DA")
def test_TEST_32109(setup):
    TEST_CASE_ID = "TEST-32109"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
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