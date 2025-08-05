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
    
    def is_dot_present(self):
        """
        Returns True if get_dot_count() is greater than 0, else False.
        """
        return self.get_dot_count() > 0

    def count_dots(self):
        """
        Returns the number of visible divs with class 'dots' on the screen.
        """
        dot_locators = self.page.locator("div.dots")
        return dot_locators.count()
    
    def get_dot_count(self):
        """
        Returns the number of dots:
        - If 'div.count' is present, returns its integer value.
        - Otherwise, returns the count of 'div.dots' elements.
        """
        count_locator = self.page.locator("div.count")
        if count_locator.count() > 0:
            # 'div.count' is present, get its integer value
            count_text = count_locator.inner_text().strip()
            try:
                return int(count_text)
            except ValueError:
                return 0
        else:
            # Fallback: count 'div.dots' elements
            dot_locators = self.page.locator("div.dots")
            return dot_locators.count()