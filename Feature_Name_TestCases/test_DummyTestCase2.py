import time
from Execution_Templates.Table_Execution_Template import TableExecutionTemplate
import allure


@allure.feature("Buy-In Feature")
@allure.story("test_DummyTestCase2: Rated Buy-In")
@allure.title("test_DummyTestCase2 Rated Buy-In Test")
def test_DummyTestCase2(setup,request):
    # Initialize base test and page objects
    tbd = TableExecutionTemplate(setup, "TEST-1999")
    request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]

    table_data = tbd.sessions_tab.sessions_tab_extract_table_data()
    print("Extracted Table Data:", table_data)

    table_data = tbd.games_tab.games_tab_extract_table_data()
    print("Extracted Table Data:", table_data)
