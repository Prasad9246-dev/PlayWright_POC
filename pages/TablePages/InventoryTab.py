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
        """Returns the locator for the Inventory tab.
        Author:
            Prasad Kamble
        """
        return self.inventory_tab_selector

    def scan_button(self):
        """Returns the locator for the Scan button.
        Author:
            Prasad Kamble
        """
        return self.scan_button_selector

    def adjust_button(self):
        """Returns the locator for the Adjust button.
        Author:
            Prasad Kamble
        """
        return self.adjust_button_selector

    def select_reason_option(self):
        """Returns the locator for the Select Reason dropdown.
        Author:
            Prasad Kamble
        """
        return self.select_reason_selector

    def reason_others_option(self):
        """Returns the locator for the 'Others' reason option.
        Author:
            Prasad Kamble
        """
        return self.reason_others_selector

    def confirm_button(self):
        """Returns the locator for the Confirm button.
        Author:
            Prasad Kamble
        """
        return self.confirm_button_selector