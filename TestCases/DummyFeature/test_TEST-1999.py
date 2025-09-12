import allure
from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_TEST_1999(setup):
    TEST_CASE_ID = "TEST-1999"
    FEATURE_NAME = "DummyFeature"
    ppb = PPExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = ppb.config.get("build_version")
    status = "Fail"
    remarks = ""
    try:
        ppb.configuration_login.navigate_to_configuration("Configuration")
        status = "Pass"  

    except Exception as e:
        remarks = str(e)
        print(f"Failed to void hand in test: {remarks}")
        # try:
        #     ppb.void_game()
        # except Exception as ve:
        #     print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        ppb.test_case_report.write_test_result(
            FEATURE_NAME,
            TEST_CASE_ID,
            BUILD_VERSION,
            status,
            remarks
        )