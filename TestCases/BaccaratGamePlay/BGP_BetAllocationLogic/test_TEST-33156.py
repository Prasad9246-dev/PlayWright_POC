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
    ppb.configuration_login.navigate_to_configuration("Configuration")
    request.node.ppb = ppb

    # Use setup (the Page object) for UI actions
    page = setup

    # Step 2: Click Business Rules tab
    page.get_by_role("tab", name="Business Rules").click()
    time.sleep(5)

    # Step 3: Click Create button if it exists
    print("Step 3: Checking for 'Create' button...")
    try:
        create_button = page.get_by_role("button", name="Create", exact=True)
        if create_button.is_visible():
            print("'Create' button is visible. Clicking...")
            create_button.click()
            time.sleep(5)
        else:
            print("'Create' button is not visible. Skipping click.")
    except Exception as e:
        print(f"Exception while clicking 'Create' button: {e}")
        # Fallback: Try clicking directly as per recorded step
        print("Trying direct click using recorded step...")
        try:
            page.get_by_role("button", name="Create", exact=True).click()
            print("Clicked 'Create' button using recorded step.")
            time.sleep(5)
        except Exception as ex:
            print(f"Failed to click 'Create' button: {ex}")

    # Step 4: Click and assert Bet Attribution tab
    try:
        bet_attr_tab = page.get_by_text("Bet Attribution")
        if bet_attr_tab.is_visible():
            bet_attr_tab.click()
            print("Bet Attribution tab is visible and clicked: successful assertion")
            assert True, "Bet Attribution tab is visible and clickable: successful assertion"
        else:
            print("Bet Attribution tab is not visible: failed assertion")
            assert False, "Bet Attribution tab is not visible: failed assertion"
    except Exception as e:
        print(f"Exception while clicking 'Bet Attribution' tab: {e}")
        assert False, "Bet Attribution tab is not clickable: failed assertion"

    # Step 5: Click and assert Display chip owner on game
    try:
        display_chip_owner = page.get_by_text("Display chip owner on game")
        if display_chip_owner.is_visible():
            display_chip_owner.click()
            print("Display chip owner on game is visible and clicked: successful assertion")
            assert True, "Display chip owner on game is visible and clickable: successful assertion"
        else:
            print("Display chip owner on game is not visible: failed assertion")
            assert False, "Display chip owner on game is not visible: failed assertion"
    except Exception as e:
        print(f"Exception while clicking 'Display chip owner on game': {e}")
        assert False, "Display chip owner on game is not clickable: failed assertion"

