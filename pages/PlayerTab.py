class PlayerTab:
    def __init__(self, page):
        self.page = page
        self.Players_TAB = self.page.get_by_role('tab', name="Players")
        self.Enter_Player_ID = self.page.get_by_placeholder("Enter Player ID")
        self.first_row_first_col_selector = 'tbody.mdc-data-table__content tr[role="row"]:nth-of-type(1) td:nth-of-type(1)'
        self.clock_in_player_button = self.page.get_by_role("button", name="Clock-In Player")

    def dropdown_button(self):
        return self.page.get_by_role('button', name='arrow_drop_down', exact=True)

    def menu_item_close(self):
        return self.page.get_by_role('menuitem', name='Close')

    def menu_item_open(self):
        return self.page.get_by_role('menuitem', name='Open')

    def confirm_button(self):
        return self.page.get_by_role('button', name='Confirm')

    def table_dashboard_button(self):
        return self.page.get_by_role('button', name='Table Dashboard')

    def table_controls_menu_item(self):
        return self.page.get_by_role('menuitem', name='Table Controls')

    def expire_chips_button(self):
        return self.page.get_by_role('button', name='Expire Chips It expires all')

    def close_button(self):
        return self.page.get_by_role('button', name='Close')

    def player_card_position(self, position_num):
        """
        Returns a Playwright locator for a player card by position number.
        """
        selector = f'#player-card--0\\.{position_num}'
        return self.page.locator(selector)