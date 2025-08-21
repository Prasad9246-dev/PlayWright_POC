from tests.BaseTest import BaseTest
from utils.excel_reader import get_buyin_data
from GameSkeleton.BuyIN import BuyIN
import time

def test_run_TEST_14009(setup):
    """
    Main test function for TEST-14009. Executes buy-in, wager, card, chip actions,
    and verifies Casino W/L on Inventory and Games tabs.
    """
    base_test = BaseTest(setup, "TEST-14009")
    table_ip = base_test.tableIP
    chips_df = base_test.chips_df

    buyin_data = base_test.buyin_data
    result = base_test.buyin_processor.process_buyins(table_ip, buyin_data, chips_df)
    time.sleep(2)

    # Process wagers after buy-in
    wager_data = base_test.wager_data
    wager_data_result = base_test.wager_processor.process_wagers(table_ip, result, wager_data)
    time.sleep(2)

    # Draw cards and press shoe button
    base_test.card_processor.draw_cards_and_shoe_press(base_test.card_data, table_ip)
    time.sleep(2)

    # Click on Reveal Button
    base_test.View_Table_Tab.reveal_button.click()
    time.sleep(2)

    # Get Chip ID for Denomination
    chip_ID = ",".join(base_test.table_actions.get_chip_ids_for_denom(chips_df, "100"))
    time.sleep(2)

    # Move Chip on P3
    base_test.table_actions.chip_move_antenna(table_ip, "P3", chip_ID, "true")
    time.sleep(2)

    # Draw 5th Card
    base_test.card_processor.deal_cards_and_activate_shoe(table_ip, "2s")
    time.sleep(2)

    # Take Chip from B3
    base_test.take_bets_processor.take(table_ip, wager_data_result, base_test.take_bets_data)
    time.sleep(2)

    # Take Chip from P3
    base_test.table_actions.chip_move_antenna(table_ip, "P3", chip_ID, "false")
    time.sleep(2)

    # Verify Casino W/L on Inventory tab
    expected_wl = "1000"  # Replace with the expected value for Casino W/L
    open_inventory_tab_and_verify_casino_wl(setup, expected_wl)
    time.sleep(2)
    open_games_tab_and_verify_casino_wl(setup, expected_wl)
    time.sleep(2)

def open_inventory_tab_and_verify_casino_wl(page, expected_wl):
    """
    Opens the Inventory tab, verifies Casino W/L value, and prints success or fail message.
    """
    inventory_tab_locator = page.get_by_role("tab", name="Inventory")
    inventory_tab_locator.wait_for(state="visible", timeout=5000)
    inventory_tab_locator.click()
    time.sleep(2)

    # Wait for the table to load (adjust selector as needed)
    page.wait_for_selector(".mat-mdc-table", timeout=10000)
    time.sleep(2)

    # Debug: Print how many matching cells are found
    cells = page.locator(
        ".mat-mdc-cell.mdc-data-table__cell.cdk-cell.position-relative.cdk-column-application-app-PLAYER_DASH_LABELS-CASINO_WL > .wd-flex"
    )
    cell_count = cells.count()
    print(f"Found {cell_count} Casino W/L cells on Inventory tab.")

    if cell_count == 0:
        print("Casino W/L cell not found on Inventory tab. Check selector or page data.")
        assert False, "Casino W/L cell not visible on Inventory tab"
        return

    wl_cell = cells.first
    wl_cell.wait_for(state="visible", timeout=5000)
    actual_wl = wl_cell.text_content().strip()
    if actual_wl == expected_wl:
        print(f"Inventory tab Casino W/L is correct: {actual_wl}. Success.")
    else:
        print(f"Inventory tab Casino W/L is incorrect: {actual_wl}. Expected: {expected_wl}.")
    assert actual_wl == expected_wl, f"Inventory tab Casino W/L mismatch: {actual_wl} != {expected_wl}"

def open_games_tab_and_verify_casino_wl(page, expected_wl):
    """
    Opens the Games tab, verifies Casino W/L value, and prints success or fail message.
    """
    games_tab_locator = page.get_by_role("tab", name="Games")
    games_tab_locator.wait_for(state="visible", timeout=5000)
    games_tab_locator.click()
    time.sleep(2)
    wl_cell = page.locator(
        ".mat-mdc-cell.mdc-data-table__cell.cdk-cell.position-relative.cdk-column-application-app-PLAYER_DASH_LABELS-CASINO_WL > .wd-flex"
    ).first
    assert wl_cell.is_visible(), "Casino W/L cell not visible on Games tab"
    actual_wl = wl_cell.text_content().strip()
    if actual_wl == expected_wl:
        print(f"Games tab Casino W/L is correct: {actual_wl}. Success.")
    else:
        print(f"Games tab Casino W/L is incorrect: {actual_wl}. Expected: {expected_wl}.")
    assert actual_wl == expected_wl, f"Games tab Casino W/L mismatch: {actual_wl} != {expected_wl}"