from Utilites.TableUtils.TableActions import TableActions
class OverrideTab:
    def __init__(self, page, feature_name):
        self.page = page
        self.override_tab_selector = self.page.get_by_role('tab', name="Override")
        self.void_hand_button = self.page.get_by_role("button", name="Void Hand")
        self.table_actions = TableActions(page, feature_name)

    def click_void_hand(self):
        """
        Clicks the 'Void Hand' button if it is enabled.
        Returns True if clicked, False otherwise.
        Author:
            Prasad Kamble
        """
        self.table_actions.navigate_to_tab(self.override_tab_selector, wait_time=2000)
        if self.void_hand_button.is_enabled():
            self.void_hand_button.click()
            return True
        return False