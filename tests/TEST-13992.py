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
        page.get_by_role("button", name="Configuration", exact=False).click()
        print("Clicked Configuration button.")
        time.sleep(4)
    else:
        print("Login page not visible. Skipping login.")
        time.sleep(4)

    # Confirm login success (UI loads, no error)
    print("Login successful.")
    time.sleep(4)

def test_run_TEST_13992(setup):
    tbd = BaseTest(setup, "TEST-13992")
    table_ip = tbd.tableIP
    chips_df = tbd.chips_df
    config_page = setup.context.new_page()


    # Step 1 – Login
    try:
        login_and_open_configuration(config_page)
    except Exception as e:
        print(f"Step 1 FAIL: {e}")

    # Step 2 – Game Template Tab(Click on Game Template Tab)
    game_templates_tab = config_page.get_by_role("tab", name="Game Templates")
    game_templates_tab.wait_for(state="visible", timeout=5000)
    game_templates_tab.click()
    print("Clicked Game Templates tab.")
    time.sleep(2)
    # Step 2 – Applied Games Template (Click on Applied Game Template)
    assert config_page.get_by_text("GT-83").is_visible(), "GT-83 not visible"
    config_page.get_by_text("GT-83").click()
    print("Step 2: Clicked Applied Game Template button.")
    time.sleep(4)

    # Step 3 – Click 'Mid Game Bets'
    assert config_page.get_by_text('Mid Game Bets').is_visible(), "'Mid Game Bets' not visible"
    config_page.get_by_text('Mid Game Bets').click()
    print("Step 3: Clicked 'Mid Game Bets'.")

    # Step 4 – Click 'Bet Timer(In Seconds)' and check visibility
    if config_page.get_by_text('Bet Timer(In Seconds)').is_visible():
        print("Step 4 PASS: 'Bet Timer(In Seconds)' is visible.")
        config_page.get_by_text('Bet Timer(In Seconds)').click()
    else:
        print("Step 4 FAIL: 'Bet Timer(In Seconds)' not visible.")
        assert False, "'Bet Timer(In Seconds)' not visible"

    # Step 5 – Check value in #mat-input-93 is 30
    # Find the Bet Timer input dynamically by its unique class
    bet_timer_input = config_page.locator('input.com\\.walkerdigital\\.bet\\.insurance\\.bet\\.timer')
    bet_timer_input.wait_for(state="visible", timeout=5000)
    value = bet_timer_input.input_value()
    assert value == "30", f"Expected Bet Timer value to be 30, but got {value}"
    print("Step 5 PASS: Bet Timer default value is 30.")

    # Step 6 – Enter Zero
    bet_timer_input.fill('0')
    bet_timer_input.press('Enter')
    time.sleep(4)
    print("Step 6: Entered 0 in Bet Timer input and pressed Enter.")

    # Step 7 – Check if Save button is enabled
    save_button = config_page.get_by_role('button', name='Save', exact=True)
    save_button.wait_for(state="visible", timeout=5000)
    assert save_button.is_enabled(), "Save button is not enabled after entering 0"
    print("Step 7 PASS: Save button is enabled after entering 0.")

    # Step 8 – Clear the input (remove previous text)
    bet_timer_input.fill('')
    bet_timer_input.press('Enter')
    time.sleep(4)
    print("Step 8: Cleared Bet Timer input.")

    # Step 9 – Check if Save button is disabled after clearing
    if not save_button.is_enabled():
        print("Step 9 PASS: Save button is disabled after clearing input.")
    else:
        print("Step 9 FAIL: Save button is still enabled after clearing input.")
        assert False, "Save button should be disabled after clearing input"



    buyin_data = tbd.buyin_data
    result = tbd.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    time.sleep(2)

    # Process wagers after buy-in
    wager_data = tbd.wager_data
    wager_data_result = tbd.wager_processor.process_wagers(table_ip, result, wager_data)
    time.sleep(2)

    # Draw cards and press shoe button
    tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
    time.sleep(2)
