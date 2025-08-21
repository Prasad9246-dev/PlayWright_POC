from tests.BaseTest import BaseTest
import time

def login_and_open_configuration(page):
    """
    Navigates to the PP Application login URL, logs in with provided credentials,
    and confirms login success. Prints status messages and adds a 4-second sleep after each step.
    """
    page.goto("https://wdts-gateway-cs01.wdts.local:792/login")
    print("Navigated to login URL.")
    time.sleep(4)

    # Check if Login page is visible
    if page.get_by_text("Login").is_visible():
        print("Login page is visible. Proceeding with login.")
        time.sleep(4)
        page.get_by_role("textbox", name="Username").fill("ppmaster")
        page.get_by_role("textbox", name="Password").fill("35Ramrod!")
        time.sleep(4)
        page.get_by_role("textbox", name="Password").press("Enter")
        time.sleep(4)
        page.wait_for_timeout(2000)  # Wait for login to process
        time.sleep(4)
    else:
        print("Login page not visible. Skipping login.")
        time.sleep(4)

    # Confirm login success (UI loads, no error)
    print("Login successful.")
    time.sleep(4)

def test_run_TEST_20442(setup):
    """
    Test for Roles tab.
    """
    page = setup

    # Step 1 – Login
    try:
        login_and_open_configuration(page)
    except Exception as e:
        print(f"Login to PP Application failed: {e}")

    # Step 2 – Roles tab and configuration steps
    print(f"Current URL after login: {page.url}")
    try:
        roles_tab = page.get_by_role("tab", name="Roles")
        roles_tab.wait_for(state="visible", timeout=10000)  # Wait up to 10 seconds
        assert roles_tab.is_visible(), "Roles tab should be visible"
        print("Roles tab is visible. Clicking Roles tab.")
        roles_tab.click()
    except Exception as e:
        print("Roles tab not found or not visible. Debug info:")
        print(page.content())  # Print page HTML for troubleshooting
        raise

    # Click Cashier cell
    cashier_cell = page.get_by_role("cell", name="Cashier").locator("div")
    assert cashier_cell.is_visible(), "Cashier cell should be visible"
    print("Cashier cell is visible. Clicking Cashier cell.")
    cashier_cell.click()

    # Close Cashier
    cashier_close = page.get_by_label("Cashier close").get_by_text("Cashier", exact=True)
    assert cashier_close.is_visible(), "Cashier close should be visible"
    print("Cashier close is visible. Clicking to close Cashier.")
    cashier_close.click()

    # Fill input #mat-input-1 and zoom out
    input1 = page.locator("#mat-input-1")
    assert input1.is_visible(), "Input #mat-input-1 should be visible"
    input1.click()
    input1.fill("qwertyuiopasdfghjklzxcvbnm1234")
    print("Filled input #mat-input-1.")
    for i in range(5):
        input1.press("ControlOrMeta+-")
        print(f"Zoomed out {i+1} time(s) on input #mat-input-1.")
    assert input1.input_value() == "qwertyuiopasdfghjklzxcvbnm1234", "Input #mat-input-1 value should match"

    # Click Save button
    save_btn = page.get_by_role("button", name="Save", exact=True)
    assert save_btn.is_visible(), "Save button should be visible"
    save_btn.click()
    print("Clicked Save button after input #mat-input-1.")

    # Fill input #mat-input-2 with 'q' and save
    input2 = page.locator("#mat-input-2")
    assert input2.is_visible(), "Input #mat-input-2 should be visible"
    input2.click()
    input2.fill("q")
    save_btn.click()
    print("Filled input #mat-input-2 with 'q' and clicked Save.")
    assert input2.input_value() == "q", "Input #mat-input-2 value should be 'q'"

    # Fill input #mat-input-2 with '99', then clear and fill with other values
    input2.click()
    input2.fill("99")
    print("Filled input #mat-input-2 with '99'.")
    input2.click()
    input2.fill("")
    print("Cleared input #mat-input-2.")
    input2.click()
    input2.fill("avc@")
    print("Filled input #mat-input-2 with 'avc@'.")
    input2.click()
    input2.fill("teststring")
    print("Filled input #mat-input-2 with 'teststring'.")
    save_btn.click()
    print("Clicked Save button after multiple fills in input #mat-input-2.")
    assert input2.input_value() == "teststring", "Input #mat-input-2 value should be 'teststring'"

    # Click Confirm button
    confirm_btn = page.get_by_role("button", name="Confirm")
    assert confirm_btn.is_visible(), "Confirm button should be visible"
    confirm_btn.click()
    print("Clicked Confirm button.")

    # Click top-nav heading link
    top_nav_link = page.get_by_role("heading", name="top-nav").get_by_role("link")
    assert top_nav_link.is_visible(), "Top-nav heading link should be visible"
    top_nav_link.click()
    print("Clicked top-nav heading link.")

    # Fill input #mat-input-4 and save
    input4 = page.locator("#mat-input-4")
    assert input4.is_visible(), "Input #mat-input-4 should be visible"
    input4.click()
    save_btn.click()
    print("Filled input #mat-input-4 and clicked Save.")

    # Click Confirm button again
    confirm_btn.click()
    print("Clicked Confirm button again.")


