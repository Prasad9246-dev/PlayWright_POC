class UIUtils:
    def __init__(self, page):
        self.page = page

    def click(self, locator):
        """Clicks the given locator."""
        self.page.locator(locator).click()
        
    def click_tab(self, selector):
        """Clicks the tab specified by the selector string."""
        self.page.locator(selector).click()

    def type_into(self, locator, text):
        """Types the given text into the locator."""
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        """Returns the text content of the locator."""
        try:
            # Wait for the element to be visible before getting text
            self.page.locator(locator).wait_for(state="visible", timeout=5000)
            return self.page.locator(locator).first.inner_text()
        except Exception as e:
            print(f"Error in get_text: {e}")
            return None
        

    def is_visible(self, locator):
        """Checks if the locator is visible on the page."""
        try:
            return self.page.locator(locator).is_visible()
        except Exception:
            return False

    def wait_for_visible(self, locator, timeout=5000):
        """Waits for the locator to be visible."""
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)

    def wait_for_enabled(self, locator, timeout=5000):
        """Waits for the locator to be enabled."""
        self.page.locator(locator).wait_for(state="enabled", timeout=timeout)
        
        
    def is_game_id_incremented_by_one(previousGameID, CurrentGameID):
        """
        Returns True if CurrentGameID is exactly 1 greater than previousGameID, else False.
        """
        try:
            prev_id = int(previousGameID)
            curr_id = int(CurrentGameID)
            return curr_id == prev_id + 1
        except ValueError:
            print("Game IDs are not valid integers.")
            return False
        
        
    def get_first_row_as_dict(self):
        """
        Returns the first row of the table as a dictionary mapping column names to cell values.
        Assumes table[role='table'] is unique on the page.
        """
        table = self.page.locator("table[role='table']")
        # Get all column headers
        headers = table.locator("thead tr th").all_inner_texts()
        # Get all cell values from the first row
        cells = table.locator("tbody tr:first-child td").all_inner_texts()
        # Map headers to cell values (skip empty headers/cells if needed)
        result = {}
        for header, cell in zip(headers, cells):
            header = header.strip()
            if header:  # skip empty header columns
                result[header] = cell.strip()
        return result