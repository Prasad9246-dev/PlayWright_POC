import pandas as pd
import time
from Utilites.TableUtils.TableActions import TableActions

class GamesTab:
    
    def __init__(self, page, feature_name):
        self.page = page
        self.table_actions = TableActions(page, feature_name)
        self.games_tab_locator = self.page.get_by_role('tab', name="Games")
        self.games_tab_table = self.page.locator('table.mat-mdc-table')
        self.header_selector = 'thead tr th'
        self.row_selector = 'tbody tr[role="row"]'
        self.first_row_first_column = self.page.locator("table[role='table'] tbody tr:first-child td:first-child")
        self.games_table_locator = self.page.locator("table[role='table']")
        self.table_header_locator = self.page.locator("thead tr th")
        self.table_body_locator = self.page.locator("tbody tr:first-child td")
        
    def get_first_row_first_column_text(self):
        """
        Returns the value of the first column, first row in the games table.
        Author:
            Prasad Kamble
        """
        try:
            # Locate the first row and then the first cell (td)
            self.first_cell = self.page.locator("table[role='table'] tbody tr[role='row']:nth-child(1) td:nth-child(2)")
            self.first_cell.wait_for(state="visible", timeout=5000)
            value = self.first_cell.inner_text().strip()
            print(f"First row, first column value: '{value}'")
            return value
        except Exception as e:
            print(f"Error in get_first_cell_value: {e}")
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
        headers = self.games_table_locator.locator(self.table_header_locator).all_inner_texts()
        # Get all cell values from the first row
        cells = self.games_table_locator.locator(self.table_body_locator).all_inner_texts()
        # Map headers to cell values (skip empty headers/cells if needed)
        result = {}
        for header, cell in zip(headers, cells):
            header = header.strip()
            if header:  # skip empty header columns
                result[header] = cell.strip()
        return result
    
    def games_tab_extract_table_data(self):
        """
        Extracts all rows and columns from the games details table and returns a list of dictionaries,
        where each dictionary maps column headers to cell values.

        Returns:
            list[dict]: List of row dictionaries.

        Author:
            Prasad Kamble
        """
        # Use the selector for the details table (role='table')
        table = self.games_table_locator
        # Extract headers
        headers = table.locator(self.header_selector).all_text_contents()
        clean_headers = [h.strip() for h in headers]
        # Extract rows
        rows = table.locator(self.row_selector)
        data = []
        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td").all_text_contents()
            row_dict = dict(zip(clean_headers, [cell.strip() for cell in cells]))
            data.append(row_dict)
        return data
    
    def extract_nested_details_table_data(self):
        """
        Extracts all rows and columns from the first nested details table inside the expanded row
        and returns a list of dictionaries, where each dictionary maps column headers to cell values.

        Returns:
            list[dict]: List of row dictionaries.

        Author:
            Prasad Kamble
        """
        time.sleep(4)
        # Find the first nested table inside the expanded details row
        nested_table = self.page.locator("tr.game-detail-row td app-game-details table[role='table']").first
        # Extract headers
        headers = nested_table.locator("thead tr th").all_text_contents()
        clean_headers = [h.strip() for h in headers]
        # Extract rows
        rows = nested_table.locator("tbody tr[role='row']")
        data = []
        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td").all_text_contents()
            row_dict = dict(zip(clean_headers, [cell.strip() for cell in cells]))
            data.append(row_dict)
        return data
    