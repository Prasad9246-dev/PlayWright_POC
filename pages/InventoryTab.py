class InventoryTab:
    def __init__(self, page):
        self.page = page
        self.inventory_tab_selector = self.page.get_by_role('tab', name="Inventory")
        self.scan_button_selector = self.page.get_by_role('button', name='Scan')
        self.adjust_button_selector = self.page.get_by_role('button', name='Adjust')
        self.select_reason_selector = self.page.get_by_role("combobox")
        self.reason_others_selector = self.page.locator("text=Others").first
        self.confirm_button_selector = self.page.get_by_role('button', name='Confirm')

    def inventory_tab(self):
        return self.inventory_tab_selector

    def scan_button(self):
        return self.scan_button_selector

    def adjust_button(self):
        return self.adjust_button_selector

    def select_reason_option(self):
        return self.select_reason_selector

    def reason_others_option(self):
        return self.reason_others_selector

    def confirm_button(self):
        return self.confirm_button_selector