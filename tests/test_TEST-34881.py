from time import time
from base_tests.TBDBaseTest import TBDBaseTest
import allure

@allure.feature("CF_TableUI")
@allure.story("TEST-34881: CF_TableUI")
@allure.title("TEST-34881 To verify that the user is able to search the player with the PlayerId, firstName,LastName,PPID with the keyvalue properties for the active player search for the WDTS Client")
def test_34881(setup,request):
    
    # Initialize base test and get required data
    tbd = TBDBaseTest(setup, "TEST-34881")
    page = setup
    # request.node.tbd = tbd
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df
    # Step 1: Click 'Players' tab
    tbd.table_actions.clock_in_player("Players_TAB",1,"6001")
    time.sleep(4)

    # if tbd.table_actions.player_tab.Players_TAB.is_visible():
    #     tbd.table_actions.player_tab.Players_TAB.click()
    #     print("SUCCESS: 'Players' tab clicked.")
    #     tbd.screenshot_util.attach_screenshot(name="Players Tab Click")
    #     tbd.screenshot_util.attach_text("Clicked 'Players' tab.", name="Verification Message")
    # else:
    #     print("FAILED: 'Players' tab not visible.")
    #     tbd.screenshot_util.attach_screenshot(name="Players Tab Not Visible")
    #     tbd.screenshot_util.attach_text("'Players' tab not visible.", name="Verification Message")
    #     assert False, "'Players' tab not visible."
    #     time.sleep(2)  # Wait for tab to load
    # # Step 2: Click clock-in icon for first player card
    # # Step 1: Try to click the 3rd button with empty text (Player clock-in)
    # clock_in_buttons = page.get_by_role("button").filter(has_text="")
    # if clock_in_buttons.nth(2).is_visible():
    #     clock_in_buttons.nth(2).click()
    #     print("SUCCESS: Player clock-in button is visible and clicked.")
    #     allure.attach("Player clock-in button is visible and clicked.", name="Clock-In Log")
    #     assert True, "SUCCESS: Player clock-in button is visible and clicked."
    # else:
    #     print("FAILED: Player is not clocked-In. Skipping rest of the test.")
    #     allure.attach("Player is not clocked-In. Skipping rest of the test.", name="Clock-In Log")
    #     assert False, "Player is not clocked-In. Skipping rest of the test."
    # Recorded Step: Click the element if it is visible
    # Example: Click the 3rd button with empty text (Player clock-in)
    element = page.get_by_role("button").filter(has_text="").nth(2)
    if element.is_visible():
        element.click()
        print("SUCCESS: Element is visible and clicked.")
        allure.attach("Element is visible and clicked.", name="Element Click Log")
        assert True, "SUCCESS: Element is visible and clicked."
    else:
        print("FAILED: Element not visible, skipping click.")
        allure.attach("Element not visible, skipping click.", name="Element Click Log")
        assert False, "FAILED: Element not visible, skipping click."
    # Step 2: Click on MID header and assert visibility
    mid_header = page.get_by_text("MID", exact=True)
    if mid_header.is_visible():
        mid_header.click()
        print("SUCCESS: MID header is visible and clicked.")
        allure.attach("MID header is visible and clicked.", name="MID Header Log")
        assert True, "SUCCESS: MID header is visible and clicked."
    else:
        print("FAILED: MID header not visible.")
        allure.attach("MID header not visible.", name="MID Header Log")
        assert False, "FAILED: MID header not visible."

    # Step 3: Click on MID No. button
    mid_no_btn = page.get_by_role("button", name="MID No.")
    if mid_no_btn.is_visible():
        mid_no_btn.click()
        print("SUCCESS: MID No. button is visible and clicked.")
        allure.attach("MID No. button is visible and clicked.", name="MID No. Button Log")
        assert True, "SUCCESS: MID No. button is visible and clicked."
    else:
        print("FAILED: MID No. button not visible.")
        allure.attach("MID No. button not visible.", name="MID No. Button Log")
        assert False, "FAILED: MID No. button not visible."

    # Step 4: Enter MID No. in textbox
    mid_textbox = page.get_by_role("textbox", name="MID")
    if mid_textbox.is_visible():
        mid_textbox.fill("123")
        print("SUCCESS: MID textbox is visible and filled with '123'.")
        allure.attach("MID textbox is visible and filled with '123'.", name="MID Textbox Log")
        assert True, "SUCCESS: MID textbox is visible and filled."
    else:
        print("FAILED: MID textbox not visible.")
        allure.attach("MID textbox not visible.", name="MID Textbox Log")
        assert False, "FAILED: MID textbox not visible."

    # Step 5: Click Ok button to save
    ok_btn = page.get_by_role("button", name="Ok")
    if ok_btn.is_visible():
        ok_btn.click()
        print("SUCCESS: Ok button is visible and clicked.")
        allure.attach("Ok button is visible and clicked.", name="Ok Button Log")
        assert True, "SUCCESS: Ok button is visible and clicked."
    else:
        print("FAILED: Ok button not visible.")
        allure.attach("Ok button not visible.", name="Ok Button Log")
        assert False, "FAILED: Ok button not visible."

    # Step 6: Verify entered MID No. is visible
    mid_value = page.get_by_text("123")
    if mid_value.is_visible():
        mid_value.click()
        print("SUCCESS: Entered MID No. '123' is visible after update.")
        allure.attach("Entered MID No. '123' is visible after update.", name="MID Value Log")
        assert True, "SUCCESS: Entered MID No. '123' is visible after update."
    else:
        print("FAILED: Entered MID No. '123' not visible after update.")
        allure.attach("Entered MID No. '123' not visible after update.", name="MID Value Log")
        assert False, "FAILED: Entered MID No. '123' not visible after update."