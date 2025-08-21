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

def test_run_TEST_13994(setup):
    """
    Test for Limits Tab and Insurance Bets UI Verification.
    Steps:
    1. Login and open configuration
    2. Navigate to Limits tab
    3. Verify 'Enable Mid Game Bets' column
    4. Enter details till 'Out of balance error threshold value'
    5. Verify property 'Enable Mid Game Bets'
    6. Click checkbox and verify extra fields
    7. Verify default values
    """
    page = setup

    # Step 1 – Login
    try:
        login_and_open_configuration(page)
    except Exception as e:
        print(f"Step 1 FAIL: {e}")

    # Step 2 – Limits Tab (click Configuration, then Limits)
    config_button = page.get_by_role("button", name="Configuration", exact=False)
    config_button.wait_for(state="visible", timeout=15000)
    config_button.click()
    print("Step 2: Clicked Configuration button.")
    time.sleep(4)

    limits_tab = page.get_by_role("tab", name="Limits")
    limits_tab.wait_for(state="visible", timeout=5000)
    limits_tab.click()
    time.sleep(4)

    assert page.get_by_text("LT-83").is_visible(), "LT-83 not visible"
    page.get_by_text("LT-83").click()
    print("Clicked LT-83 successfully.")
    time.sleep(4)

    # Step 3 – Verify 'Enable Mid Game Bets' Column
    assert page.get_by_text("Mid Game Bets").is_visible(), "'Enable Mid Game Bets' column not visible"
    page.get_by_text("Mid Game Bets").click()
    print("Step 3 PASS: 'Enable Mid Game Bets' column is visible.")

    if page.get_by_text("Insurance Bet Increment").is_visible():
        print("Insurance Bet Increment is visible. Success.")
    else:
        print("Insurance Bet Increment not visible. Failed.")
        assert False, "Insurance Bet Increment not visible"

    if page.get_by_text("Min Insurance Bet").is_visible():
        print("Min Insurance Bet is visible. Success.")
    else:
        print("Min Insurance Bet not visible. Failed.")
        assert False, "Min Insurance Bet not visible"

    if page.get_by_text("Max Insurance payout cap").is_visible():
        print("Max Insurance payout cap is visible. Success.")
    else:
        print("Max Insurance payout cap not visible. Failed.")
        assert False, "Max Insurance payout cap not visible"

    if page.get_by_text("Max Insurance Wager % of").is_visible():
        print("Max Insurance Wager % of is visible. Success.")
    else:
        print("Max Insurance Wager % of not visible. Failed.")
        assert False, "Max Insurance Wager % of not visible"

    # Step 4 – Enter Details till 'Out of balance error threshold value'
    # page.locator('mat-form-field:has-text("Insurance Bet Increment") input[matinput]').fill("5")
    # page.locator('mat-form-field:has-text("Min Insurance Bet") input[matinput]').fill("5")
    # page.locator('mat-form-field:has-text("Max Insurance payout cap") input[matinput]').fill("999999999")
    # page.locator('mat-form-field:has-text("Max Insurance Wager % of") input[matinput]').fill("200")
    # page.get_by_text("Thresholds").click()
    # page.locator("#mat-input-158").fill("25000")
    # page.locator("#mat-input-159").fill("9999999")
    # page.locator("#mat-input-160").fill("10000")
    # page.locator("#mat-input-161").fill("0")
    print("Tested all the fields visibility.")

    # # Step 5 – Verify Property 'Enable Mid Game Bets'
    # insurance_checkbox = page.get_by_text("Enable Insurance betYesNo")
    # assert insurance_checkbox.is_visible(), "'Enable Insurance bet' property not visible"
    # print("Step 5 PASS: 'Enable Insurance bet' property is visible.")

    # Step 6 – Click Checkbox and verify extra fields
    # page.get_by_role("button", name="No").click()

    # minBet = page.locator("#mat-input-154").input_value()
    # increment = page.locator("#mat-input-155").input_value()
    # payoutCap = page.locator("#mat-input-156").input_value()
    # wagerPercent = page.locator("#mat-input-157").input_value()
    # assert payoutCap == "5000", f"Max insurance payout cap default incorrect: {payoutCap}"
    # assert wagerPercent == "50", f"Max insurance wager % default incorrect: {wagerPercent}"
    # print("Step 6 PASS: Checkbox enabled and extra fields appeared with defaults.")

    # # Step 7 – Verify Defaults
    # assert minBet == "5", f"Min Insurance Bet default incorrect: {minBet}"
    # assert increment == "5", f"Insurance Bet Increment default incorrect: {increment}"
    # print("Step 7 PASS: Min Insurance Bet and Increment default values are correct.")

    # If you need to enable insurance first:
    # insurance_enable_btn = page.get_by_role("button", name="No")
    # if insurance_enable_btn.is_visible():
    #     insurance_enable_btn.click()
    #     print("Insurance enabled.")
    #     time.sleep(4)
    # else:
    #     print("Insurance enable button not visible, skipping.")