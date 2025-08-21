from pages.ViewTableTab import ViewTableTab

class UIUtils:
    def __init__(self, page):
        self.page = page
        self.view_table_tab = ViewTableTab(self.page)

    def click_to_element(self, element_selector):
        """Clicks the given element."""
        if isinstance(element_selector, str):
            self.page.locator(element_selector).click()
        else:
            element_selector.click()

    def fill_element(self, locator, text):
        """Types the given text into the locator or selector."""
        if isinstance(locator, str):
            self.page.locator(locator).fill(text)
        else:
            locator.fill(text)
        
    def press_enter(self, locator):
        """Presses Enter on the given locator or selector."""
        if isinstance(locator, str):
            self.page.locator(locator).press("Enter")
        else:
            locator.press("Enter")

    def get_text(self, locator):
        """Returns the text content of the locator."""
        try:
            # Wait for the element to be visible before getting text
            return locator.inner_text()
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
    
    def is_quick_buy_in_present(self):
        """
        Checks if the 'QUICK BUY IN' option is present on the screen.
        Prints a message if present.
        Returns True if present, False otherwise.
        """
        try:
            if self.view_table_tab.quick_buy_in().is_visible():
                print("QUICK BUY IN Option is present on screen")
                return True
            else:
                print("QUICK BUY IN Option is NOT present on screen")
                return False
        except Exception:
                    print("QUICK BUY IN Option is NOT present on screen")
                    return False
            # Check if QUICK BUY IN is present
            
    def is_buy_in_button_present(self):
        """
        Checks if the Buy-In confirm button is present on the screen.
        Prints a message if present.
        Returns True if present, False otherwise.
        """
        try:
            if self.view_table_tab.buy_in_confirm_button().is_visible():
                print("Buy-In Confirm Button is present on screen")
                return True
            else:
                print("Buy-In Confirm Button is NOT present on screen")
                return False
        except Exception:
                    print("Buy-In Confirm Button is NOT present on screen")    