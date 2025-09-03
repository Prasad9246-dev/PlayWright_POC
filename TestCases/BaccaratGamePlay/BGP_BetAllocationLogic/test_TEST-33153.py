from ExecutionTemplates.TableExecutionTemplate import TableExecutionTemplate
import allure
from playwright.sync_api import Page
import time
 
@allure.feature("Bet Allocation Logic")
@allure.story("TEST-33153: Bet Allocation Logic")
@allure.title("TEST-33153 To verify the ownership of chips when player places more than one stack on a single seat")
def test_33153(setup):
    # Initialize base test and get required data
    tbd = TableExecutionTemplate(setup, "TEST-33153","BGP_BetAllocationLogic")
    table_ip = tbd.config["tableIP"]
    chips_df = tbd.chips_df
 
    # Navigate to Games tab and get previous Game ID
    tbd.table_actions.navigate_to_tab(tbd.games_tab.GAMES_TAB)
    previous_game_id = tbd.games_tab.get_first_row_first_column_text()
 
    # Process buy-ins
    buyin_result = tbd.buyin_processor.process_buyins(table_ip, tbd.buyin_data, chips_df)
    print("Buy-In Results:")
    for entry in buyin_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Chips ID: {entry['chips_ID']}")
 
    # Process wagers
    wager_result = tbd.wager_processor.process_wagers(table_ip, buyin_result, tbd.wager_data)
    print("Wager Results:")
    for entry in wager_result:
        print(f"Player: {entry['player']}, Denom: {entry['denom']}, Antenna: {entry['antenna']}, Chips ID: {entry['chips_ID']}")
 
    # Draw cards and press shoe button
    tbd.card_processor.draw_cards_and_shoe_press(tbd.card_data, table_ip)
 
    # Process payouts
    tbd.payout_processor.process_payouts(table_ip, tbd.payout_data, chips_df)
    time.sleep(5)
 
    # Recorded steps: Table Dashboard and Chip Details navigation, then extract table
    tbd.page.get_by_role("button", name="Table Dashboard").click()
    tbd.page.get_by_role("menuitem", name="Chip Details").click()
    # Extract the datatable
    datatable = tbd.page.locator("table.table-chip-details")

    # Get headers
    headers = datatable.locator("thead tr th")
    header_texts = [headers.nth(i).inner_text().strip() for i in range(headers.count())]
    print("Headers:", header_texts)

    # Get all rows
    rows = datatable.locator("tbody tr")
    for i in range(rows.count()):
        cells = rows.nth(i).locator("td")
        cell_texts = [cells.nth(j).inner_text().strip() for j in range(cells.count())]
        print(cell_texts)
        if "6001" in cell_texts:
            assert True, "Found 6001 in table row: successful assertion"
        else:
            assert False, "6001 not found in table row: failed assertion"
    # Recorded steps after table extraction
    tbd.page.get_by_role("tab", name="Games").click()
    tbd.page.get_by_role("cell", name=":31").first.click()
    cell = tbd.page.get_by_role("cell", name="Singh, Pooja (6009)", exact=True)
    cell_div_text = cell.locator("div").nth(1).inner_text().strip()
    print("Cell div text:", cell_div_text)
    if "6001" in cell_div_text:
        assert True, "Found 6001 in cell div text: successful assertion"
    else:
        assert False, "6001 not found in cell div text: failed assertion"
    tbd.page.get_by_role("button").filter(has_text="close").click()

