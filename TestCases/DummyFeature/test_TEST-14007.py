from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure
import time

@allure.feature("Player antenna logic on commission table")
@allure.story("Insurance on Banker antenna disables Player antenna")
@allure.title("Player antenna should remain off when Banker antenna has insurance on commission table")
def test_TEST_14007(setup):
    TEST_CASE_ID = "TEST-14007"
    FEATURE_NAME = "DummyFeature"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = tbd.config.get("build_version")
    status = "Pass"
    remarks = ""
    try:
        time.sleep(2)

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