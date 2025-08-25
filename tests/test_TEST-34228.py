import time
from base_tests.PPBaseTest import PPBaseTest
import allure

@allure.feature("CF_TableUI")
@allure.story("TEST-34228: CF_TableUI")
@allure.title("TEST-34228 To verify that the user is able to search the player with the PlayerId, firstName,LastName, with the keyvalue properties for the CMS player search on  the WDTS Client")
def test_34228(setup,request):
    # Initialize base test and get required data
    PP = PPBaseTest(setup, "TEST-34228")
    page = setup

    pp_browser = PP.configuration_actions.drill_down(PP,setup,PP.config["tableIP"])
    time.sleep(5)

    # Step 5: Click menu (more_vert)
    menu_icon = pp_browser.get_by_role("menu").filter(has_text="more_vert")
    if menu_icon.is_visible():
        menu_icon.click()
        print("SUCCESS: Menu icon clicked.")
        allure.attach("Menu icon clicked.", name="Menu Log")
        assert True, "SUCCESS: Menu icon was visible and clicked."
    else:
        print("FAILED: Menu icon not visible.")
        allure.attach("Menu icon not visible.", name="Menu Log")
        assert False, "FAILED: Menu icon not visible."

    # Step 6: Click Player Search menu item
    player_search_menu = pp_browser.get_by_role("menuitem", name="Player Search")
    if player_search_menu.is_visible():
        player_search_menu.click()
        print("SUCCESS: Player Search menu item clicked.")
        allure.attach("Player Search menu item clicked.", name="Player Search Log")
        assert True, "SUCCESS: Player Search menu item was visible and clicked."
    else:
        print("FAILED: Player Search menu item not visible.")
        allure.attach("Player Search menu item not visible.", name="Player Search Log")
        assert False, "FAILED: Player Search menu item not visible."

    # Step 7: Check Player Search header is visible
    player_search_header = pp_browser.get_by_role("heading", name="Player Search")
    if player_search_header.is_visible():
        print("SUCCESS: Player Search header is visible.")
        allure.attach("Player Search header is visible.", name="Header Log")
        assert True, "SUCCESS: Player Search header is visible."
    else:
        print("FAILED: Player Search header not visible.")
        allure.attach("Player Search header not visible.", name="Header Log")
        assert False, "FAILED: Player Search header not visible."

    # Step 8: Click Player ID to open dropdown
    player_id_dropdown = pp_browser.get_by_text("Player ID")
    player_id_dropdown.click()
    print("Clicked 'Player ID' to open dropdown.")
    allure.attach("Clicked 'Player ID' to open dropdown.", name="Dropdown Log")

    # Step 9: Validate dropdown options and click each
    dropdown_options = ["First Name", "Last Name", "PP ID", "Player ID"]
    for option in dropdown_options:
        # Use get_by_role("option", name=...) for strict matching
        option_locator = pp_browser.get_by_role("option", name=option)
        if option_locator.is_visible():
            print(f"SUCCESS: Option '{option}' is visible in dropdown.")
            allure.attach(f"Option '{option}' is visible in dropdown.", name="Dropdown Option Log")
            assert True, f"SUCCESS: Option '{option}' is visible in dropdown."
        else:
            print(f"FAILED: Option '{option}' not visible in dropdown.")
            allure.attach(f"Option '{option}' not visible in dropdown.", name="Dropdown Option Log")
            assert False, f"FAILED: Option '{option}' not visible in dropdown."
    # --- End Player Search Dropdown Validation Test Steps ---
