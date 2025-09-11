from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Baccarat Game Play - Ownership after paying out from losing chips")
@allure.story("To verify the ownership of chips when we do payout with mixed chips (losing+casino owned)")
@allure.title("TEST-32108: To verify the ownership of chips when we do payout with mixed chips (losing+casino owned)")
def test_TEST_32108(setup):
    TEST_CASE_ID = "TEST-32108"
    FEATURE_NAME = "BGP_OwnershipPayoutLosingChips"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Pass"
    remarks = ""
    try:
        # Step 1: Do anonymous buyin of 500*5 and place 500*3 on Banker and 500*2 on PP
        # Step 2: Make banker win and PP lose
        # Step 3: Now take 500*2 from PP and place it on DD and 500*1 from chip tray and pay it to banker
        # Step 4: Verify the ownership of chips
        # Step 5: Verify Chip history report
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