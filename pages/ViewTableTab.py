class ViewTableTab:
    
    def __init__(self, page):
        self.page = page
        
    TAKE_PLAYER = "TAKEPLAYER"
    VIEW_TABLE = "View Table"
    PLAYER_SEARCH = "Player Search"
    BUY_IN_CONFIRM_BUTTON = "button.wd-dd-button.button-confirm.tick"

    def view_table_tab(self):
        return self.page.get_by_role('tab', name=self.VIEW_TABLE)

    def seat_section(self, seat_number):
        return self.page.locator('section').filter(has_text=str(seat_number)).locator('div').first
    
    def player_search_box(self):
        return self.page.get_by_role('textbox', name=self.PLAYER_SEARCH)

    def buy_in_confirm_button(self):
        return self.page.locator(self.BUY_IN_CONFIRM_BUTTON)
