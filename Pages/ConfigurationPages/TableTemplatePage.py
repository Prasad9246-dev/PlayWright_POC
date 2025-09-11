class TableTemplatePage():
    def __init__(self, page):
        self.page = page
        self.table_templates_tab = self.page.get_by_role("tab", name="Table Templates")
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)
        self.table_template_name_textbox = self.page.get_by_role("textbox", name="Name")
        self.site_select_combobox = self.page.get_by_role("combobox", name="Site")
        self.table_type_combobox = self.page.get_by_role("combobox", name="Table type")
        self.game_type_combobox = self.page.get_by_role("combobox", name="Game type")
        self.baccarat_option = self.page.get_by_role("option", name="Baccarat")
        self.game_template_combobox = self.page.get_by_role("combobox", name="Game Template")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.confirm_button = self.page.get_by_role("button", name="Confirm")
        self.created_success_message = self.page.get_by_text("Created successfully.", exact=False)

    def get_site_option(self, site_name):
        return self.page.get_by_role("option", name=site_name, exact=True)
    
    def get_table_type_option(self, table_type_value):
        return self.page.get_by_role("option", name=table_type_value, exact=True)
    
    def get_game_template_option(self, game_template_name):
        return self.page.get_by_role("option", name=game_template_name, exact=True)