import time
import allure
from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate

@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_TEST_1999(setup,request):
    ppb = PPExecutionTemplate(setup, "TEST-1999")
    request.node.tbd = ppb
    ppb.configuration_actions.drill_down(setup, ppb.config["tableIP"])