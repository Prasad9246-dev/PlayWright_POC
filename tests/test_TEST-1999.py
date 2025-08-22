import time
from base_tests.TBDBaseTest import TBDBaseTest
import allure


@allure.feature("Buy-In Feature")
@allure.story("TEST-1999: Rated Buy-In")
@allure.title("TEST-1999 Rated Buy-In Test")
def test_1999(setup,request):
    # Initialize base test and page objects
    tbd = TBDBaseTest(setup, "TEST-1999")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]

    table_data = tbd.sessions_tab.sessions_tab_extract_table_data()
    print("Extracted Table Data:", table_data)

    table_data = tbd.games_tab.games_tab_extract_table_data()
    print("Extracted Table Data:", table_data)
