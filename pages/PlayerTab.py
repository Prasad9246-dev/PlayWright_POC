class PlayerTab:
    def __init__(self, page):
        self.page = page
        self.Players_TAB = self.page.get_by_role('tab', name="Players")

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