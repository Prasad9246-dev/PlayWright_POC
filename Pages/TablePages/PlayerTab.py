class PlayerTab:
    def __init__(self, page):
        self.page = page
        self.Players_TAB = self.page.get_by_role('tab', name="Players")
        self.Enter_Player_ID = self.page.get_by_placeholder("Enter Player ID")
        self.first_row_first_col_selector = 'tbody.mdc-data-table__content tr[role="row"]:nth-of-type(1) td:nth-of-type(1)'
        self.clock_in_player_button = self.page.get_by_role("button", name="Clock-In Player")
        self.clock_out_button = self.page.get_by_role("button", name="Clock-Out")
        self.clock_out_close_button = self.page.get_by_label("Clock-Outclose").get_by_role("button", name="Clock-Out")
        
        # Manual Rating selectors
        self.seat_A = self.page.locator(
    'mat-button-toggle button[name="seat"]:has(span.mat-button-toggle-label-content:has-text("A"))'
).first
        self.player_id_textbox = self.page.get_by_role("textbox", name="Enter Player ID/Name")
        self.first_player_item = self.page.locator(".searched-players__list__item").first
        self.start_time = self.page.get_by_label("Manual Rating Formclose").get_by_text("Start Time")
        self.stop_time = self.page.get_by_text("Stop Time")
        self.minus_hour_btn = self.page.get_by_role("button", name="Minus a hour")
        self.set_btn = self.page.get_by_role("button", name="Set")
        self.cash_buyin_textbox = self.page.get_by_role("textbox", name="Cash Buy In")
        self.average_bet_textbox = self.page.get_by_role("textbox", name="Average Bet")
        self.casino_win_loss_textbox = self.page.get_by_role("textbox", name="Casino W/L")
        self.mid_textbox = self.page.get_by_role("textbox", name="MID")
        self.submit_btn = self.page.get_by_role("button", name="Submit")
        self.save_btn = self.page.get_by_role("button", name="Save")

    def dropdown_button(self):
        """Returns the locator for the dropdown button.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('button', name='arrow_drop_down', exact=True)

    def menu_item_close(self):
        """Returns the locator for the Close menu item.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('menuitem', name='Close')

    def menu_item_open(self):
        """Returns the locator for the Open menu item.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('menuitem', name='Open')

    def confirm_button(self):
        """Returns the locator for the Confirm button.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('button', name='Confirm')

    def table_dashboard_button(self):
        """Returns the locator for the Table Dashboard button.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('button', name='Table Dashboard')

    def table_controls_menu_item(self):
        """Returns the locator for the Table Controls menu item.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('menuitem', name='Table Controls')

    def expire_chips_button(self):
        return self.page.get_by_role('button', name='Expire Chips It expires all')

    def close_button(self):
        """Returns the locator for the Close button.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_role('button', name='Close')

    def player_card_position(self, position_num):
        """
        Returns a Playwright locator for a player card by position number.
        Author:
            Prasad Kamble
        """
        selector = f'#player-card--0\\.{position_num}'
        return self.page.locator(selector)
    
    def player_card_dot(self, seat_num):
        """
        Returns the locator for the dot button inside the player card for the given seat number.
        Author:
            Prasad Kamble
        """
        selector = f'[id="player-card--0\\.{seat_num}"]'
        return self.page.locator(selector).get_by_role("button").nth(3)
    
    def select_seat(self, seat_num):
        """
        Returns the locator for the seat label like '2A'.
        Args:
            seat_num (str or int): The seat number to select.
        Author:
            Prasad Kamble
        """
        return self.page.get_by_text(f"{seat_num}A")
    
    def get_seat_A_locator(self):
        """
        Returns the locator for seat 'A', handling both radio (2.4) and button (2.3) versions.
        Author:
            Prasad Kamble
        """
        locator_radio = self.page.get_by_role("radio", name="A", exact=True)
        if locator_radio.count() > 0:
            return locator_radio
        locator_button = self.page.get_by_role("button", name="A", exact=True)
        if locator_button.count() > 0:
            return locator_button