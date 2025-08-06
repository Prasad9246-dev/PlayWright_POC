class ViewTableTab:
    def __init__(self, page):
        self.page = page
        self.view_table_tab_selector = self.page.get_by_role('tab', name="View Table")
        self.player_search_box_selector = self.page.get_by_role('textbox', name="Player Search")
        self.buy_in_confirm_button_selector = self.page.locator("button.wd-dd-button.button-confirm.tick")
        self.dot_locator = self.page.locator("div.dots")
        self.count_locator = self.page.locator("div.count")
        self.quick_buy_in_selector = self.page.get_by_text('QUICK BUY IN')

    def view_table_tab(self):
        return self.view_table_tab_selector

    def seat_section(self, seat_number):
        return self.page.locator('section').filter(has_text=str(seat_number)).locator('div').first

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
        