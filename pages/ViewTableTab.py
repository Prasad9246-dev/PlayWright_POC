class ViewTableTab:
    def __init__(self, page):
        self.page = page
        self.view_table_tab_selector = self.page.get_by_role('tab', name="View Table")
        self.player_search_box_selector = self.page.get_by_role('textbox', name="Player Search")
        self.buy_in_confirm_button_selector = self.page.locator("button.wd-dd-button.button-confirm.tick")
        self.dot_locator = self.page.locator("div.dots")
        self.count_locator = self.page.locator("div.count")
        self.quick_buy_in_selector = self.page.get_by_text('QUICK BUY IN')
        # self.BuyIn_GreenBar = self.page.locator("#dealerAndAggrAmount")
        self.Transfer = self.page.get_by_role("menuitem", name="Transfer")
        self.Change = self.page.get_by_role("menuitem", name="Change")
        self.transfer_ConfirmButton = self.page.locator("button.wd-dd-button.button-confirm.confirm")
        self.transfer_Header = self.page.get_by_text("Transfer")
        self.Change_Header = self.page.get_by_text("Change", exact=True)
        self.dealer_and_aggr_amount_button = self.page.locator("#dealerAndAggrAmount")
        self.BuyIn_Close = self.page.get_by_role("button", name="close")
        self.Change_ConfirmButton = self.page.locator("button.wd-dd-button.button-confirm.confirm")
        self.SessionsTab = self.page.get_by_role("tab", name="Sessions")
        self.seat_1_Player = self.page.locator("#seat__1").get_by_text("1", exact=True)
        self.Player = self.page.get_by_role("img", name="Cash chips")
        self.update_player_search = self.page.get_by_role('textbox')
        self.reveal_button = self.page.get_by_text('REVEAL')

    def view_table_tab(self):
        return self.view_table_tab_selector

    def seat_section(self, seat_number):
        return self.page.locator(f'div.seat__seat-wrapper:has(button.seat.pos__{seat_number})').click()

    def player_search_box(self):
        return self.player_search_box_selector

    def buy_in_confirm_button(self):
        return self.buy_in_confirm_button_selector

    def is_dot_present(self):
        """
        Returns True if get_dot_count() is greater than 0, else False.
        """
        return self.get_dot_count() > 0

    def count_dots(self):
        """
        Returns the number of visible divs with class 'dots' on the screen.
        """
        return self.dot_locator.count()

    def get_dot_count(self):
        """
        Returns the number of dots:
        - If 'div.count' is present, returns its integer value.
        - Otherwise, returns the count of 'div.dots' elements.
        """
        if self.count_locator.count() > 0:
            count_text = self.count_locator.inner_text().strip()
            try:
                return int(count_text)
            except ValueError:
                return 0
        else:
            return self.dot_locator.count()

    def quick_buy_in(self):
            """
            Returns the locator for the 'QUICK BUY IN' button/text.
            """
            return self.quick_buy_in_selector

    def click_verify_if_visible(self):
        """
        Clicks the 'Verify' button if it is visible and prints 'success'.
        """
        verify_button = self.page.get_by_role("button", name="Verify")
        if verify_button.is_visible():
            print("Verify button is available on Screen successfully.")
            verify_button.click()

    def click_update_if_visible(self):
        """
        Clicks the 'Update' button if it is visible and prints a success message.
        """
        update_button = self.page.get_by_role("button", name="Update")
        if update_button.is_visible():
            print("Update button is available on Screen successfully.")
            update_button.click()

    def update_player_and_verify(self, player_id: str = "6001"):
        """
        Updates a player by searching for the player ID, clicking the 'Update' button if visible,
        and then clicking the 'Verify' button if it exists and is visible.

        Args:
            player_id (str): The player ID to search for. Defaults to "6001".
        """
        # Fill the player search box and press Enter
        self.update_player_search.fill(player_id)
        self.update_player_search.press("Enter")
        self.page.wait_for_timeout(1000)  # Wait for search results to load

        # Click the Verify button if visible
        verify_button = self.page.get_by_role("button", name="Verify")
        if verify_button.is_visible():
            print("Verify button is available on Screen successfully.")
            verify_button.click()
        else:
            print("Verify button is not available on Screen.")
