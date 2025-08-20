class CasinoManager():
    def __init__(self, page):
        self.page = page
        self.manual_ratings_tab = self.page.get_by_role("tab", name="Manual Ratings")

    def site_button(self, site_name):
        """Returns the locator for the Site button (e.g., 'Site-83')."""
        return self.page.get_by_role("button", name=site_name)

    def ga_button(self, ga_name):
        """Returns the locator for the GA button (e.g., 'GA-')."""
        return self.page.get_by_role("button", name=ga_name)

    def oa_text(self, oa_name):
        """Returns the locator for the OA text (e.g., 'OA-')."""
        return self.page.get_by_text(oa_name)

    def pit_text(self, pit_name):
        """Returns the locator for the Pit text (e.g., 'Pit-')."""
        return self.page.get_by_text(pit_name)