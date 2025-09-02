import pandas as pd

class SessionsTab:
    def __init__(self, page, feature_name, table_actions=None):
        from Utilites.TableUtils.TableActions import TableActions
        self.table_actions = table_actions
        self.feature_name = feature_name
        self.page = page
        self.session_tab =  self.page.get_by_role("tab", name="Sessions")
        self.sessions_tab_table = self.page.locator('table.mat-mdc-table')
        self.header_selector = 'thead tr th'
        self.row_selector = 'tbody tr[role="row"]'
        # Manual Rating selectors
        self.create_manual_rating_btn = self.page.get_by_role("button", name="Create Manual Rating")
        self.seat_number = self.page.get_by_text("Seat Number")
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
        
        
    def get_seat_option(self, seat_no):
        """
        Returns Playwright locator for the seat dropdown option.

        Args:
            seat_no (str or int): Seat number to select.

        Author: Prasad Kamble
        """
        return self.page.get_by_role("option", name=str(seat_no))
    
    def sessions_tab_extract_table_data(self):
        """
        Extracts all rows and columns from the table and returns a pandas DataFrame with cleaned column names.
        
        Author:
            Prasad Kamble
        """
        self.table_actions.navigate_to_tab(self.session_tab)
        table = self.sessions_tab_table
        headers = table.locator(self.header_selector).all_text_contents()
        # Remove ' import_export ' from headers
        clean_headers = [h.replace(' import_export ', '').strip() for h in headers]
        data = []
        rows = table.locator(self.row_selector)
        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator('td').all_text_contents()
            row_dict = dict(zip(clean_headers, [cell.strip() for cell in cells]))
            data.append(row_dict)
        df = pd.DataFrame(data)
        return df