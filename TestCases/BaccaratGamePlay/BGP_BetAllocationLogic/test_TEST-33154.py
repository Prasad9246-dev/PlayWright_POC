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

    # Step 4: Assert "Attribution" text is available and interact with radio buttons
    print("Step 4: Waiting for 'Attribution' text to be visible and clickable...")
    page.wait_for_timeout(2000)  # Wait for UI to update

    # Click and assert Attribution label
    try:
        page.get_by_text("Attribution", exact=True).click()
        print("Clicked 'Attribution' label: successful assertion")
        assert True, "Attribution label is clickable: successful assertion"
    except Exception as e:
        print(f"Could not click 'Attribution' label: {e}")
        assert False, "Attribution label is not clickable: failed assertion"

    # Click and assert Stack Pay Order label
    try:
        page.get_by_text("Stack Pay Order", exact=True).click()
        print("Clicked 'Stack Pay Order' label: successful assertion")
        assert True, "Stack Pay Order label is clickable: successful assertion"
    except Exception as e:
        print(f"Could not click 'Stack Pay Order' label: {e}")
        assert False, "Stack Pay Order label is not clickable: failed assertion"

    # Click and assert Ownership followed by Stack label
    try:
        page.get_by_text("Ownership followed by Stack").click()
        print("Clicked 'Ownership followed by Stack' label: successful assertion")
        assert True, "Ownership followed by Stack label is clickable: successful assertion"
    except Exception as e:
        print(f"Could not click 'Ownership followed by Stack' label: {e}")
        assert False, "Ownership followed by Stack label is not clickable: failed assertion"

    # Click and assert Ownership label
    try:
        page.get_by_text("Ownership", exact=True).click()
        print("Clicked 'Ownership' label: successful assertion")
        assert True, "Ownership label is clickable: successful assertion"
    except Exception as e:
        print(f"Could not click 'Ownership' label: {e}")
        assert False, "Ownership label is not clickable: failed assertion"

    # Check Stack Pay Order radio button
    print("Step 5: Checking 'Stack Pay Order' radio button...")
    stack_pay_radio = page.get_by_role("radio", name="Stack Pay Order", exact=True)
    stack_pay_radio.check()
    if stack_pay_radio.is_checked():
        print("'Stack Pay Order' radio is checked and visible: successful assertion")
    else:
        print("'Stack Pay Order' radio is not checked or not visible: failed assertion")
    assert stack_pay_radio.is_checked(), "Stack Pay Order radio is checked and visible: successful assertion"

    # Step 6: Check Ownership followed by Stack radio and assert visibility
    print("Step 6: Checking 'Ownership followed by Stack' radio button...")
    ownership_stack_radio = page.get_by_role("radio", name="Ownership followed by Stack")
    ownership_stack_radio.check()
    if ownership_stack_radio.is_checked():
        print("'Ownership followed by Stack' radio is checked and visible: successful assertion")
    else:
        print("'Ownership followed by Stack' radio is not checked or not visible: failed assertion")
    assert ownership_stack_radio.is_checked(), "Ownership followed by Stack radio is checked and visible: successful assertion"

    # Step 7: Check Ownership radio and assert visibility
    print("Step 7: Checking 'Ownership' radio button...")
    ownership_radio = page.get_by_role("radio", name="Ownership", exact=True)
    ownership_radio.check()
    if ownership_radio.is_checked():
        print("'Ownership' radio is checked and visible: successful assertion")
    else:
        print("'Ownership' radio is not checked or not visible: failed assertion")
    assert ownership_radio.is_checked(), "Ownership radio is checked and visible: successful assertion"
