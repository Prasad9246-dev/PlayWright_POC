class TableTemplatePage():
    def __init__(self, page):
        self.page = page
        self.table_templates_tab = self.page.get_by_role("tab", name="Table Templates")
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)
        self.table_template_name_textbox = self.page.get_by_role("textbox", name="Name")
        self.site_select_combobox = self.page.get_by_role("combobox", name="Site", exact=True)
        self.table_type_combobox = self.page.get_by_role("combobox", name="Table type")
        self.game_type_combobox = self.page.get_by_role("combobox", name="Game type")
        self.baccarat_option = self.page.get_by_role("option", name="Baccarat")
        self.game_template_combobox = self.page.get_by_role("combobox", name="Game Template")
        self.limits_tab = self.page.get_by_role("tab", name="Limits")
        self.chip_sets_tab = self.page.get_by_text("Chip Sets", exact=True)
        self.save_button = self.page.get_by_role("button", name="Save")
        self.confirm_button = self.page.get_by_role("button", name="Confirm")
        self.created_success_message = self.page.get_by_text("Created successfully.", exact=False)

    def get_site_option(self, site_name):
        return self.page.get_by_role("option", name=site_name, exact=True)
    
    def get_table_type_option(self, table_type_value):
        return self.page.get_by_role("option", name=table_type_value, exact=True)
    
    def get_game_template_option(self, game_template_name):
        return self.page.get_by_role("option", name=game_template_name, exact=True)
    
    def click_all_chipset_list_items(self):
        list_items = self.page.locator('mat-list-item .mat-line')
        for i in range(list_items.count()):
            list_items.nth(i).click()
            
    def get_limit_template_option(self, limit_template_name):
        return self.page.get_by_text(limit_template_name, exact=True)