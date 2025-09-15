from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Manual Rating Feature")
@allure.story("test_DummyTestCase3: Manual Rating Submission")
@allure.title("test_DummyTestCase3: Manual Rating Submission Test")
def test_TEST_14007(setup):
    TEST_CASE_ID = "TEST-14007"
    FEATURE_NAME = "DummyFeature"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Pass"
    remarks = ""
    try:
        table_ip = tbd.config.get("tableIP")
        tbd.configuration_api.update_template([("com.wdts.bt.require.player.verification", "false")], tbd.config.get("pp_application_url"), table_ip, "BUSINESS_RULES")
  
    except Exception as e:
        status = "Fail"
        remarks = str(e)
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        tbd.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )