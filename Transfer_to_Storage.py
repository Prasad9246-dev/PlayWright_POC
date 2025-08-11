import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    # Move chips to dealer (example: click on chip, then select dealer)
    # This logic may need to be adapted to your actual UI selectors and chip IDs
    chip_id = "e00540011226b05d"  # Example chip id, replace as needed
    page.get_by_role("button", name="TT").click()  # Click on TT antenna/chip source
    page.get_by_role("menuitem", name="Move").click()
    page.get_by_role("menuitem", name="DEALER").click()
    page.wait_for_timeout(1000)

    # Click on the green bar (assuming it's a button or element with a unique role or name)
    page.get_by_role("button", name="(0)").click()
    page.get_by_role("menuitem", name="Transfer").click()

    # Click on Storage option in the transfer menu
    page.get_by_role("menuitem", name="Storage").click()
    page.wait_for_timeout(500)

    # Check if 'Transfer' header exists, print success if found
    if page.get_by_text("Transfer").is_visible():
        print("Success: 'Transfer' header is present on the page.")

    # Confirm the transfer
    page.get_by_role("button", name="Confirm").click()