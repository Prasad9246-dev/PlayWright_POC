class GamesTab:
    
    def __init__(self, page):
        self.page = page
        self.GAMES_TAB = self.page.get_by_role('tab', name="Games")
    
    GAME_ID_CELL = "table[role='table'] tbody tr:first-child td:nth-child(2)"
    TABLE_LOCATOR = "table[role='table']"
    TABLE_HEADER_LOCATOR = "thead tr th"
    TABLE_BODY_LOCATOR = "tbody tr:first-child td"

    def get_first_row_first_column_text(self):
        """
        Returns the text content of the first row, first column cell in the table.
        """
        # locator = "table[role='table'] tbody tr:first-child td:nth-child(2)"  # 2nd <td> is the first data column
        try:
            self.page.locator(self.GAME_ID_CELL).wait_for(state="visible", timeout=5000)
            text = self.page.locator(self.GAME_ID_CELL).inner_text()
            print(f"First row, first column text: '{text}'")
            return text
        except Exception as e:
            print(f"Error in get_first_row_first_column_text: {e}")
            return None
               
    def get_first_row_as_dict(self):
        """
        Returns the first row of the table as a dictionary mapping column names to cell values.
        Assumes table[role='table'] is unique on the page.
        """
        # table = self.page.locator("table[role='table']")
        # Get all column headers
        headers = self.TABLE_LOCATOR.locator(self.TABLE_HEADER_LOCATOR).all_inner_texts()
        # Get all cell values from the first row
        cells = self.TABLE_LOCATOR.locator(self.TABLE_BODY_LOCATOR).all_inner_texts()
        # Map headers to cell values (skip empty headers/cells if needed)
        result = {}
        for header, cell in zip(headers, cells):
            header = header.strip()
            if header:  # skip empty header columns
                result[header] = cell.strip()
        return result