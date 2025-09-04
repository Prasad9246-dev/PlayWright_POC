from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
from Utilites.ExcelRead.TestReportWriter import TestReportWriter
from datetime import datetime
import allure

@allure.feature("Player antenna logic on commission table")
@allure.story("Insurance on Banker antenna disables Player antenna")
@allure.title("Player antenna should remain off when Banker antenna has insurance on commission table")
def test_TEST_14007(setup):
    TEST_CASE_ID = "TEST-14007"
    FEATURE_NAME = "PlayWright_POC"
    tbd = TableExecutionTemplate(setup, TEST_CASE_ID, FEATURE_NAME)
    status = "Pass"
    remarks = ""
    try:
        # response = tbd.configuration_api.get_table_info(tbd.config.get("tableIP"))
        # game_template = response['gameTemplate']
        # print(game_template)
        # template_id = tbd.configuration_db.get_game_template_id(tbd.config.get("tableIP"), game_template)
        # print(template_id)
        # current_template = tbd.configuration_api.get_current_template(tbd.config.get("tableIP"),tbd.config.get("pp_application_url"),"TABLE")
        # print(current_template)
        # tbd.configuration_api.update_template([("com.wdts.back.betting.enabled", "true")],tbd.config.get("pp_application_url"),tbd.config.get("tableIP"),"TABLE")
        # print(tbd.configuration_api.get_current_template_id(tbd.config.get("pp_application_url"),tbd.config.get("tableIP"),"GAME"))
        tbd.configuration_api.update_game_template(tbd.config.get("pp_application_url"),tbd.config.get("tableIP"),[("com.wdts.manualrating.approval.criteria.averagebet", "324243")])


        # tbd.table_actions.submit_manual_rating_players_tab("6001","2","223","123","123","12223")
        # print(tbd.configuration_db.get_connection("172.41.46.23"))
        # print(tbd.configuration_db.get_connection_txndb("172.41.39.82"))
        # tbd.configuration_actions.prepend_host_entry("Z:\\PlayWright\\hosts","172.41.38.181  wdts-gateway-qa112.wdts.local")

    except Exception as e:
        status = "Fail"
        remarks = str(e)
        try:
            tbd.void_game()
        except Exception as ve:
            print(f"Failed to void hand in test: {ve}")
        raise
    finally:
        config = tbd.config
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