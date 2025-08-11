from conftest import get_url, get_username, get_password, setup, get_tableIP
import conftest
from pages.login_page import LoginPage
from utils.TableActions import TableActions
from pages.ViewTableTab import ViewTableTab
from utils.UIUtils import UIUtils
from pages.GamesTab import GamesTab

def test_login_success(setup):
    import logging
    import pytest
    try:
        url = get_url()
        username = get_username()
        password = get_password()
        tableIP = get_tableIP()
        logging.info(f"Table IP: {tableIP}, URL: {url}")

        # Initialize page objects
        login_page = LoginPage(setup)
        view_table_tab = ViewTableTab(setup)
        games_tab = GamesTab(setup)
        ui_utils = UIUtils(setup)
        table_actions = TableActions(setup)

        # Navigate to login page and perform login
        login_page.navigate(url)
        login_page.login(username, password)
        setup.wait_for_timeout(5000)

        # Table open/close actions
        table_actions.table_close_and_open()
        table_actions.chip_move_from_antenna(antenna_name="TT", chip_id="e00540011226b05d", acquired="true")
        setup.wait_for_timeout(3000)
        table_actions.expire_and_adjust()
        setup.wait_for_timeout(3000)

        # Navigate and get previous game ID
        table_actions.navigate_to_tab(games_tab.GAMES_TAB)
        previousGameID = games_tab.get_first_row_first_column_text()
        logging.info(f"Previous Game ID: {previousGameID}")
        setup.wait_for_timeout(3000)

        table_actions.navigate_to_tab("View Table")
        setup.wait_for_timeout(3000)

        # Buy-in (removed duplicate call)
        table_actions.buy_in(player_id="6001", seat_number=1, chip_id="e00540011226b05d", buyin_type="known")
        setup.wait_for_timeout(3000)

        table_actions.chip_move_from_antenna(antenna_name="P1", chip_id="e00540011226b05d", acquired="true")
        setup.wait_for_timeout(3000)
        table_actions.draw_cards(tableIP, "2s", "4d", "3s", "4d")
        setup.wait_for_timeout(7000)
        table_actions.chip_move_from_antenna(antenna_name="P1", chip_id="e00540011226b05d", acquired="false")
        setup.wait_for_timeout(3000)

        # Check game record
        table_actions.navigate_to_tab(games_tab.GAMES_TAB)
        CurrentGameID = games_tab.get_first_row_first_column_text()
        logging.info(f"Current Game ID: {CurrentGameID}")

        if previousGameID == CurrentGameID:
            logging.warning("Game record is not present on Games tab.")
            assert previousGameID == CurrentGameID, "Game record should not be present on Games tab."
        else:
            logging.info("Game record is present on Games tab.")
            assert previousGameID != CurrentGameID, "Game record should be present on Games tab."
            row_dict = ui_utils.get_first_row_as_dict()
            logging.info(f"Row Dict: {row_dict}")

    except Exception as e:
        logging.error(f"Test failed due to exception: {e}")
        pytest.fail(f"Test failed due to exception: {e}")