from datetime import datetime
import allure
from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_TEST_1999(setup):
    TEST_CASE_ID = "TEST-1999"
    FEATURE_NAME = "PlayWright_POC"
    ppb = PPExecutionTemplate(setup, "TEST-1999","PlayWright_POC")
    status = "Pass"
    remarks = ""
    try:
        ppb.configuration_login.navigate_to_configuration("Configuration")
        ppb.configuration_actions.drill_down(setup, ppb.config["tableIP"])
        ppb.logger_utils.log("Drilled down to table IP")    

    except Exception as e:
        status = "Fail"
        remarks = str(e)
        try:
            ppb.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        config = ppb.config
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