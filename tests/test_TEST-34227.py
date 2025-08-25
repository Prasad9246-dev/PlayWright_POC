from time import time
from base_tests.TBDBaseTest import TBDBaseTest
import allure

@allure.feature("CF_TableUI")
@allure.story("TEST-34227: CF_TableUI")
@allure.title("TEST-34227 To verify that the user is able to search the player with the PlayerId, firstName,LastName,PPID with the keyvalue properties for the active player search for the WDTS Client")
def test_34227(setup,request):
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TEST-34227")
    page = setup
    # request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df

    # # Navigate to Games tab and get previous Game ID
    # tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
    # previous_game_id = tbd.games_tab.get_first_row_first_column_text()

    # Step 1: Click 'Table Dashboard' button if visible
    table_dashboard_btn = page.get_by_role("button", name="Table Dashboard")
    if table_dashboard_btn.is_visible():
        table_dashboard_btn.click()
        print("SUCCESS: Clicked 'Table Dashboard' button.")
        tbd.screenshot_util.attach_screenshot(name="Table Dashboard Button Click")
        tbd.screenshot_util.attach_text("Clicked 'Table Dashboard' button.", name="Verification Message")
        assert True, "SUCCESS: 'Table Dashboard' button was visible and clicked."
    else:
        print("FAILED: 'Table Dashboard' button not visible, skipping click.")
        tbd.screenshot_util.attach_screenshot(name="Table Dashboard' button not visible")
        tbd.screenshot_util.attach_text("FAILED: 'Table Dashboard' button not visible, skipping click.", name="Verification Message")
        assert False, "FAILED: 'Table Dashboard' button not visible."

    # Step 2: Click 'Player Search' menu item
    player_search_menu = page.get_by_role("menuitem", name="Player Search")
    if player_search_menu.is_visible():
        player_search_menu.click()
        print("SUCCESS: Clicked 'Player Search' menu item.")
        assert True, "SUCCESS: 'Player Search' menu item was visible and clicked."
    else:
        print("FAILED: 'Player Search' menu item not visible.")
        assert False, "FAILED: 'Player Search' menu item not visible."

    # Step 3: Check 'Player Search' header is visible and click (inside dialog)
    dialog = page.get_by_role("dialog", name="Player Search")
    player_search_header = dialog.get_by_text("Player Search")
    if player_search_header.is_visible():
        print("SUCCESS: 'Player Search' header is visible in dialog.")
        assert True, "SUCCESS: 'Player Search' header is visible in dialog."
    else:
        print("FAILED: 'Player Search' header not visible in dialog.")
        assert False, "FAILED: 'Player Search' header not visible in dialog."
        
    # Step 4: Click path in Player Search dialog
    # path_locator = dialog.locator("path")
    # if path_locator.is_visible():
    #     path_locator.click()
    #     print("SUCCESS: Clicked 'path' in Player Search dialog.")
    #     assert True, "SUCCESS: 'path' locator in Player Search dialog was visible and clicked."
    #     time.sleep(4)

    #     # New Step: Click 'Player ID' option after clicking path
    #     player_id_option = page.get_by_text("Player ID", exact=True)
    #     if player_id_option.is_visible():
    #         player_id_option.click()
    #         print("SUCCESS: Clicked 'Player ID' option after path.")
    #         assert True, "SUCCESS: 'Player ID' option was visible and clicked after path."
    #     else:
    #         print("FAILED: 'Player ID' option not visible after path.")
    #         assert False, "FAILED: 'Player ID' option not visible after path."
    #     else:
    #         print("FAILED: 'path' locator in Player Search dialog not visible.")
    #         assert False, "FAILED: 'path' locator in Player Search dialog not visible."

    # Step 5: Check combobox options for 'Search By Player ID' in dialog after clicking Player ID
    combobox = dialog.get_by_role("combobox", name="Search By Player ID")
    combobox.click()  # Open the dropdown
    page.wait_for_timeout(1000)  # Wait for dropdown to render

    # Validate each option in the dropdown by role, only check visibility (do not click)
    options = [
        "Player ID",
        "First Name",
        "Last Name",
        "PP ID"
    ]
    for option_text in options:
        try:
            option_locator = page.get_by_role("option", name=option_text)
            if option_locator.is_visible():
                print(f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu.")
                assert True, f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu.."
            else:
                print(f"FAILED: Option '{option_text}' not visible in Dropdown Menu..")
                assert False, f"FAILED: Option '{option_text}' not visible in Dropdown Menu.."
        except Exception as e:
            print(f"FAILED: Exception for option '{option_text}': {e}")
            assert False, f"FAILED: Exception for option '{option_text}': {e}"

    # Extract data from Txn_db and table_db to validate database state.
    db_out = tbd.configuration_API.run_query(table_ip, "select * from ui_app_properties;")
    print(f"Database Output: {db_out}")

    # Check for 'active.player.search.options' in db_out
    if db_out and 'active.player.search.options' in str(db_out):
        print("SUCCESS: The table 'ui_app_properties' exists in table_db and contains 'active.player.search.options'.")
    else:
        print("FAILED: The table 'ui_app_properties' does not contain 'active.player.search.options'.")
    # --- End DB validation ---