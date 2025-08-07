from tests.BaseTest import BaseTest
import allure

class Test0608(BaseTest):
    def setup_method(self, setup):
        super().__init__(setup)

    def test_case(self):
        # self.setup.pause()
        # Only your test logic here, setup is already done
        self.table_actions.buy_in(player_id="6009", seat_number=1, chip_id="e00540011226b05d", buyin_type="known")
        # ...other steps...

@allure.feature("Buy-In Feature")
@allure.story("TEST-0608: Known Buy-In")
@allure.title("TEST-0608 Known Buy-In Test")        
def test_run_TEST_0608(setup):
    test = Test0608(setup)
    test.test_case()