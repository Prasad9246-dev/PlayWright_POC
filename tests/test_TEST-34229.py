from time import time
from base_tests.TBDBaseTest import TBDBaseTest
import allure

@allure.feature("CF_TableUI")
@allure.story("TEST-34229: CF_TableUI")
@allure.title("TEST-34229 To verify that the user is able to search the player with the PlayerId, firstName,LastName, with the keyvalue properties for the CMS player search on  the WDTS Client")
def test_34229(setup,request):
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TEST-34229")
    page = setup
    # request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df

    # Step 1: Click 'Players' tab
    players_tab = page.get_by_role("tab", name="Players")
    if players_tab.is_visible():
        players_tab.click()
        print("SUCCESS: 'Players' tab clicked.")
        tbd.screenshot_util.attach_screenshot(name="Players Tab Click")
        tbd.screenshot_util.attach_text("Clicked 'Players' tab.", name="Verification Message")
    else:
        print("FAILED: 'Players' tab not visible.")
        tbd.screenshot_util.attach_screenshot(name="Players Tab Not Visible")
        tbd.screenshot_util.attach_text("'Players' tab not visible.", name="Verification Message")
        assert False, "'Players' tab not visible."
        time.sleep(2)  # Wait for tab to load
    # Step 2: Click clock-in icon for first player card
    clockin_icon = page.locator('[id="player-card--0.1"] #icon-clockin-rectangle')
    if clockin_icon.is_visible():
        clockin_icon.click()
        print("SUCCESS: Clock-In icon clicked for first player card.")
        tbd.screenshot_util.attach_screenshot(name="Clock-In Icon Click")
        tbd.screenshot_util.attach_text("Clicked Clock-In icon for first player card.", name="Verification Message")
    else:
        print("FAILED: Clock-In icon not visible for first player card.")
        tbd.screenshot_util.attach_screenshot(name="Clock-In Icon Not Visible")
        tbd.screenshot_util.attach_text("Clock-In icon not visible for first player card.", name="Verification Message")
        assert False, "Clock-In icon not visible for first player card."

    # Step 3: Verify 'Clock-In Player' text is visible
    clockin_text = page.get_by_text("Clock-In Player")
    if clockin_text.is_visible():
        print("SUCCESS: 'Clock-In Player' text is visible.")
        tbd.screenshot_util.attach_text("'Clock-In Player' text is visible.", name="Verification Message")
        assert True, "'Clock-In Player' text is visible."
    else:
        print("FAILED: 'Clock-In Player' text not visible.")
        tbd.screenshot_util.attach_text("'Clock-In Player' text not visible.", name="Verification Message")
        assert False, "'Clock-In Player' text not visible."

    # # Step 4: Interact with combobox in dialog and robustly validate dropdown options
    dialog = page.get_by_role("dialog", name="Clock-In Player")
    if not dialog.is_visible():
        print("FAILED: 'Clock-In Player' dialog not visible.")
        tbd.screenshot_util.attach_text("'Clock-In Player' dialog not visible.", name="Dialog Verification")
        assert False, "'Clock-In Player' dialog not visible."
    else:
        print("SUCCESS: 'Clock-In Player' dialog is visible.")
        tbd.screenshot_util.attach_text("'Clock-In Player' dialog is visible.", name="Dialog Verification")

    # Click the 'Player search by:' label to ensure dropdown is activated
    player_search_by_label = dialog.get_by_text("Player search by:")
    if player_search_by_label.is_visible():
        player_search_by_label.click()
        print("SUCCESS: 'Player search by:' label clicked in dialog.")
        tbd.screenshot_util.attach_text("'Player search by:' label clicked in dialog.", name="Dropdown Label Verification")
        assert True, "'Player search by:' label is visible and clicked."
    else:
        print("FAILED: 'Player search by:' label not visible in dialog.")
        tbd.screenshot_util.attach_text("'Player search by:' label not visible in dialog.", name="Dropdown Label Verification")
        assert False, "'Player search by:' label not visible in dialog."

    # Validate each option in the dropdown by role, only check visibility (do not click)
    options = [
        "Player ID",
        "First Name",
        "Last Name"
    ]
    for option_text in options:
        found = False
        # Try role=option inside dialog
        try:
            option_locator = dialog.get_by_role("option", name=option_text)
            if option_locator.is_visible():
                print(f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu.")
                tbd.screenshot_util.attach_text(f"Option '{option_text}' is visible in Dropdown Menu.", name="Dropdown Option Verification")
                assert True, f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu."
                found = True
        except Exception:
            pass
        # Try role=menuitem inside dialog if not found
        if not found:
            try:
                option_locator = dialog.get_by_role("menuitem", name=option_text)
                if option_locator.is_visible():
                    print(f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu as menuitem.")
                    tbd.screenshot_util.attach_text(f"Option '{option_text}' is visible in Dropdown Menu as menuitem.", name="Dropdown Option Verification")
                    assert True, f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu as menuitem."
                    found = True
            except Exception:
                pass
        # Try text inside dialog if not found
        if not found:
            try:
                option_locator = dialog.get_by_text(option_text)
                if option_locator.is_visible():
                    print(f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu by text.")
                    tbd.screenshot_util.attach_text(f"Option '{option_text}' is visible in Dropdown Menu by text.", name="Dropdown Option Verification")
                    assert True, f"SUCCESS: Option '{option_text}' is visible in Dropdown Menu by text."
                    found = True
            except Exception:
                pass
        if not found:
            print(f"FAILED: Option '{option_text}' not visible in Dropdown Menu by any selector.")
            tbd.screenshot_util.attach_text(f"Option '{option_text}' not visible in Dropdown Menu by any selector.", name="Dropdown Option Verification")
            assert False, f"FAILED: Option '{option_text}' not visible in Dropdown Menu by any selector."
    # --- End Player Search UI Test Steps ---
