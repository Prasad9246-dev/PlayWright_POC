from tests.BaseTest import BaseTest
from utils.excel_reader import get_buyin_data
from GameSkeleton.BuyIN import BuyIN
import time

def test_run_TEST_28843(setup):
    base_test = BaseTest(setup, "TEST-28843")
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df
    base_test.Configuration_API.update_template(
    [
        ("com.wdts.bt.require.player.verification", "true")
    ],
    base_test.base_url,
    base_test.tableIP,
    "BUSINESS_RULES")
    base_test.table_actions.table_close_and_open()

    chip_ID = base_test.table_actions.get_chip_ids_for_denom(chips_df,"100")
#Move Chip on P1
    base_test.table_actions.chip_move_antenna(table_ip,"P1",chip_ID,"true")
#Click on P1
    time.sleep(2)
    base_test.View_Table_Tab.seat_1_Player.click()
    time.sleep(2)
#Click on Player
    base_test.View_Table_Tab.Player.click()
    time.sleep(2)
#Click on Update if it is visible on Screen
    base_test.View_Table_Tab.click_update_if_visible()
#Update Anonymous Player with 6001 & then click Verify
    time.sleep(2)
    base_test.View_Table_Tab.update_player_and_verify(player_id="6001")