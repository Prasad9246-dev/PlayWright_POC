class GameTemplatePage():
    def __init__(self, page):
        self.page = page
        self.game_templates_tab = self.page.get_by_role("tab", name="Game Templates")
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)
        self.game_template_name_textbox = self.page.get_by_role("textbox", name="Name")
        self.site_select_combobox = self.page.get_by_role("combobox", name="Site")
        self.table_type_combobox = self.page.get_by_role("combobox", name="Table type")
        self.game_type_combobox = self.page.get_by_role("combobox", name="Game type")
        self.baccarat_option = self.page.get_by_role("option", name="Baccarat")
        self.player_pair_option = self.page.get_by_text("Player Pair", exact=False)
        self.banker_pair_option = self.page.get_by_text("Banker Pair", exact=False)
        self.tie_option = self.page.get_by_text("Tie (TIE)", exact=True)
        self.antenna_mapping_button = self.page.get_by_role("button", name="Antenna mapping")
        self.continue_button = self.page.get_by_role("button", name="Continue", exact=False)
        self.antenna_mapping_zero = self.page.get_by_label("Antenna mapping").get_by_text("0")
        self.pp_option = self.page.get_by_text("PP", exact=True)
        self.sb1_span_option = self.page.locator("span").filter(has_text="SB1")
        self.bp_option = self.page.get_by_text("BP", exact=True)
        self.sb2_span_option = self.page.locator("span").filter(has_text="SB2")
        self.tie_option_short = self.page.get_by_text("TIE", exact=True)
        self.sb3_span_option = self.page.locator("span").filter(has_text="SB3")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.confirm_button = self.page.get_by_role("button", name="Confirm")
        self.created_success_message = self.page.get_by_text("Created successfully.", exact=False)

    def get_site_option(self, site_name):
        return self.page.get_by_role("option", name=site_name, exact=True)
    
    def get_table_type_option(self, table_type_value):
        return self.page.get_by_role("option", name=table_type_value, exact=True)