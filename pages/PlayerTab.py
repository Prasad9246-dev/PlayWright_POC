class PlayerTab:
    def __init__(self, page):
        self.page = page

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