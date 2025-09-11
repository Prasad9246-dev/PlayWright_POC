class GameTemplatePage():
    def __init__(self, page):
        self.page = page
        self.game_templates_tab = self.page.get_by_role("tab", name="Game Templates")
        self.create_button = self.page.get_by_role("button", name="Create", exact=True)
        self.game_template_name_textbox = self.page.get_by_role("textbox", name="Name")
        self.site_select_combobox = self.page.get_by_role("combobox", name="Site")
        
        
    def get_site_option(self, site_name):
        return self.page.get_by_role("option", name=site_name)