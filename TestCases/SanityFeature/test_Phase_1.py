import allure
import random
from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_Phase_1(setup):
    TEST_CASE_ID = "Phase_1"
    FEATURE_NAME = "SanityFeature"
    ppb = PPExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    BUILD_VERSION = ppb.config.get("build_version")
    status = "Fail"
    remarks = ""
    try:
        table_ip = ppb.config.get("tableIP")
        ppb.configuration_login.navigate_to_configuration("Configuration")
        game_template = f"GT-{random.randint(100, 999)}"
        limit_name = f"LT-{random.randint(100, 999)}"
        ppb.configuration_actions.create_game_template(game_template, "Site-26", table_ip)
        # ppb.configuration_actions.create_limit_template(limit_name, "Site-26", table_ip, game_template)
        # ppb.configuration_actions.create_table_template(f"TT-{random.randint(100, 999)}", "Site-26", table_ip, game_template)
        setup.pause()
        status = "Pass"

    except Exception as e:
        remarks = str(e)
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