from Utilites.TableUtils.TableActions import TableActions
import pandas as pd

class SessionsTab:
    def __init__(self, page, feature_name):
        self.table_actions = TableActions(page, feature_name)
        self.page = page
        self.sessions_tab =  self.page.get_by_role("tab", name="Sessions")
        self.sessions_tab_table = self.page.locator('table.mat-mdc-table')
        self.header_selector = 'thead tr th'
        self.row_selector = 'tbody tr[role="row"]'

    def sessions_tab_extract_table_data(self):
        """
        Extracts all rows and columns from the table and returns a pandas DataFrame with cleaned column names.
        
        Author:
            Prasad Kamble
        """
        self.table_actions.navigate_to_tab(self.sessions_tab)
        table = self.sessions_tab_table
        headers = table.locator(self.header_selector).all_text_contents()
        # Remove ' import_export ' from headers
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