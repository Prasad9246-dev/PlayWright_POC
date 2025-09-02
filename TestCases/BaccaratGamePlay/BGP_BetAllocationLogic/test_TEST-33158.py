from ExecutionTemplates.PPExecutionTemplate import PPExecutionTemplate
import allure
from playwright.sync_api import Page
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33154: Bet Allocation Logic")
@allure.title("TEST-33154 To verify the name of property -Attribution on stack pay order is changed")
def test_33154(setup,request):
    # Initialize base test and get required data
    ppb = PPExecutionTemplate(setup, "TEST-33154")
    ppb.configuration_login.navigate_to_configuration("BI Application")
    request.node.ppb = ppb

    # Use setup (the Page object) for UI actions
    page = setup

    # Step 1: Search for Configuration Audit Report
    print("Step 1: Searching for 'Configuration Audit Report'...")
    page.wait_for_timeout(1000)  # Wait for UI to be ready
    page.get_by_role("textbox", name="Search report").fill("Configuration Audit Report")
    page.wait_for_timeout(500)   # Small delay before pressing Enter
    page.get_by_role("textbox", name="Search report").press("Enter")
    print("Entered search and pressed Enter for 'Configuration Audit Report'.")

    # Step 2: Open Configuration
    page.wait_for_timeout(1500)  # Wait for search results to load
    page.get_by_text("open_in_browser Configuration").click()
    print("Clicked 'open_in_browser Configuration'.")

    # Step 3: Click PropertyProperty
    page.wait_for_timeout(1000)
    page.get_by_text("PropertyProperty").click()
    print("Clicked 'PropertyProperty'.")

    # Step 4: Search for 'Display chip owner on game start'
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="search...").fill("Display chip owner on game start")
    print("Filled search box with 'Display chip owner on game start'.")

    # Step 5: Assert 'Display chip owner on game' is visible
    page.wait_for_timeout(1000)
    display_chip_owner = page.get_by_text("Display chip owner on game")
    if display_chip_owner.is_visible():
        print("Display chip owner on game is visible: successful assertion")
        assert True, "Display chip owner on game is visible: successful assertion"
    else:
        print("Display chip owner on game is not visible: failed assertion")
        assert False, "Display chip owner on game is not visible: failed assertion"

    # # Step 6: Press Escape on Property Display chip owner combobox
    # print("Step 6: Trying to press Escape on 'Property Display chip owner' combobox...")
    # page.wait_for_timeout(500)
    # combobox = page.get_by_role("combobox", name="Property Display chip owner")
    # if combobox.is_visible():
    #     combobox.press("Escape")
    #     print("Pressed Escape on 'Property Display chip owner' combobox: successful assertion")
    #     assert True, "Pressed Escape on 'Property Display chip owner' combobox: successful assertion"
    # else:
    #     print("'Property Display chip owner' combobox not visible: failed assertion")
    #     print(page.content())  # Debug: print HTML if not found
    #     assert False, "'Property Display chip owner' combobox not visible: failed assertion"

    # # Step 7: Click Apply button
    # page.wait_for_timeout(500)
    # page.get_by_role("button", name="Apply button").click()
    # print("Clicked 'Apply button'.")