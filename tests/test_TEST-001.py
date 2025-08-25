from time import time
from base_tests.TBDBaseTest import TBDBaseTest
import allure
 
@allure.feature("CF_TableUI")
@allure.story("TEST-001: CF_TableUI")
@allure.title("TEST-001 To verify that the user is able to search the player")
def test_001(setup,request):
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TEST-001")
    page = setup
    # request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    # chips_df = tbd.chips_df

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
        tbd.screenshot_util.attach_screenshot(name="Player Search Menu Click")
    else:
        print("FAILED: 'Player Search' menu item not visible.")
        tbd.screenshot_util.attach_screenshot(name="Player Search Menu not Clicked")
        tbd.screenshot_util.attach_text("FAILED: 'Player Search' menu item not visible.", name="Verification Message")
        assert False, "FAILED: 'Player Search' menu item not visible."

    # Step 3: Check 'Player Search' header is visible and click (inside dialog)
    dialog = page.get_by_role("dialog", name="Player Search")
    player_search_header = dialog.get_by_text("Player Search")
    if player_search_header.is_visible():
        print("SUCCESS: 'Player Search' header is visible in dialog.")
        # tbd.screenshot_util.attach_screenshot(name="Player Search Menu Click")
        # tbd.screenshot_util.attach_text("SUCCESS: 'Player Search' header is visible in dialog.", name="Verification Message")
        assert True, "SUCCESS: 'Player Search' header is visible in dialog."
    else:
        print("FAILED: 'Player Search' header not visible in dialog.")
        # tbd.screenshot_util.attach_screenshot(name="Player Search Menu not Clicked")
        # tbd.screenshot_util.attach_text("FAILED: 'Player Search' header not visible in dialog.", name="Verification Message")
        assert False, "FAILED: 'Player Search' header not visible in dialog."
    # Step 4: Check combobox options for 'Search By Player ID' in dialog after clicking Player ID
    page.wait_for_timeout(1000)
    combobox = dialog.get_by_role("combobox", name="Search By Player ID")
     # Wait for dropdown to render
    combobox.click()  # Open the dropdown
    page.wait_for_timeout(1000)

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


# --- End Table Dashboard and Player Search UI Test Steps ---
# Extract data from Txn_db and table_db to validate database state.
    db_out = tbd.Configuration_API.run_query(table_ip, "select * from ui_app_properties;")
    print(f"Database Output: {db_out}")
 
    # Check for 'active.player.search.options' in db_out
    if db_out and 'active.player.search.options' in str(db_out):
        print("SUCCESS: The table 'ui_app_properties' exists in table_db and contains 'active.player.search.options'.")
    else:
        print("FAILED: The table 'ui_app_properties' does not contain 'active.player.search.options'.")
    # --- End DB validation ---