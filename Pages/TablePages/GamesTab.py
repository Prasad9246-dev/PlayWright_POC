import pandas as pd
from Utilites.TableUtils.TableActions import TableActions

class GamesTab:
    
    def __init__(self, page):
        self.page = page
        self.table_actions = TableActions(page)
        self.GAMES_TAB = self.page.get_by_role('tab', name="Games")
        self.games_tab_table = self.page.locator('table.mat-mdc-table')  # Update selector if needed
        self.header_selector = 'thead tr th'
        self.row_selector = 'tbody tr[role="row"]'
    
    GAME_ID_CELL = "table[role='table'] tbody tr:first-child td:nth-child(2)"
    TABLE_LOCATOR = "table[role='table']"
    TABLE_HEADER_LOCATOR = "thead tr th"
    TABLE_BODY_LOCATOR = "tbody tr:first-child td"

    def get_first_row_first_column_text(self):
        """
        Returns the text content of the first row, first column cell in the table.
        
        Author:
            Prasad Kamble
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
        
        Author:
            Prasad Kamble
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
    
    def games_tab_extract_table_data(self):
        """
        Extracts all rows and columns from the games table and returns a pandas DataFrame with cleaned column names.
        
        Author:
            Prasad Kamble
        """
        self.table_actions.navigate_to_tab(self.GAMES_TAB)
        table = self.games_tab_table
        headers = table.locator(self.header_selector).all_text_contents()
        clean_headers = [h.replace(' import_export ', '').strip() for h in headers]
        data = []
        rows = table.locator(self.row_selector)
        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator('td').all_text_contents()
            row_dict = dict(zip(clean_headers, [cell.strip() for cell in cells]))
            data.append(row_dict)
        df = pd.DataFrame(data)
        return df