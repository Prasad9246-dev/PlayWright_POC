class InventoryTab:
    def __init__(self, page):
        self.page = page

    def inventory_tab(self):
        return self.page.get_by_role('tab', name='Inventory')

    def scan_button(self):
        return self.page.get_by_role('button', name='Scan')
    
    def adjust_button(self):
        return self.page.get_by_role('button', name='Adjust')

    def select_reason_option(self):
        # Clicks the mat-select that contains "Select reason"
        return self.page.get_by_role("combobox")

    def reason_others_option(self):
        # Selects the "Others" option from the overlay panel (wait for it to be visible)
        return self.page.locator("text=Others").first

    def confirm_button(self):
        return self.page.get_by_role('button', name='Confirm')