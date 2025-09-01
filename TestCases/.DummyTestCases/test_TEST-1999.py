import time
import allure
from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_TEST_1999(setup):
    ppb = PPExecutionTemplate(setup, "TEST-1999","PlayWright_POC")
    ppb.configuration_login.navigate_to_configuration("Configuration")
    ppb.configuration_actions.drill_down(setup, ppb.config["tableIP"])