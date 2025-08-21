from tests.BaseTest import BaseTest
import time

# def test_run_TEST_13987(setup):
#     base_test = BaseTest(setup, "TEST-13987")

def login_and_open_configuration(page):
    """
    Navigates to the PP Application login URL, logs in with provided credentials,
    and navigates to the configuration section. Prints status messages and adds a 4-second sleep after each step.
    """
    # Navigate to the login URL
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

    # Click on Configuration button (dynamic version)
    config_button = page.get_by_role("button", name="Configuration", exact=False)
    if config_button.is_visible():
        config_button.click()
        print("Clicked on Configuration button.")
        time.sleep(4)
    else:
        print("Configuration button not visible.")
        time.sleep(4)

    # Click on appsConfiguration if visible
    apps_config = page.get_by_text("appsConfiguration")
    if apps_config.is_visible():
        print("Login successful and navigated to appsConfiguration.")
        time.sleep(4)
    else:
        print("appsConfiguration not visible after login.")
        time.sleep(4)

def select_game_template_options(page):
    """
    Navigates through the Game Templates tab and selects various game options.
    Asserts success messages if each element is visible.
    """
    assert page.get_by_role("tab", name="Game Templates").is_visible(), "Game Templates tab not visible"
    page.get_by_role("tab", name="Game Templates").click()
    print("Game Templates tab clicked successfully.")
    page.wait_for_timeout(500)

    assert page.get_by_text("GT-83").is_visible(), "GT-83 not visible"
    page.get_by_text("GT-83").click()
    print("GT-83 clicked successfully.")
    page.wait_for_timeout(500)

    assert page.get_by_text("Mid Game Bets").is_visible(), "Mid Game Bets not visible"
    page.get_by_text("Mid Game Bets").click()
    print("Mid Game Bets clicked successfully.")
    page.wait_for_timeout(500)

    assert page.get_by_text("Insurance Offer").is_visible(), "Insurance Offer not visible"
    print("Insurance Offer is visible. Success.")

    assert page.get_by_text("On Aggregate Wager").is_visible(), "On Aggregate Wager not visible"
    print("On Aggregate Wager is visible. Success.")

    assert page.get_by_text("On Largest Wager").is_visible(), "On Largest Wager not visible"
    print("On Largest Wager is visible. Success.")
    page.wait_for_timeout(500)

    assert page.get_by_text("Offer Insurance for Less").is_visible(), "Offer Insurance for Less not visible"
    print("Offer Insurance for Less is visible. Success.")
    page.wait_for_timeout(500)

    assert page.get_by_text("Insurance Bets Lose on Tie").is_visible(), "Insurance Bets Lose on Tie not visible"
    print("Insurance Bets Lose on Tie is visible. Success.")

    assert page.get_by_text("Bet Timer(In Seconds)").is_visible(), "Bet Timer(In Seconds) not visible"
    print("Bet Timer(In Seconds) is visible. Success.")

# Example pytest test function
def test_run_TEST_13987(setup):
    login_and_open_configuration(setup)
    select_game_template_options(setup)

