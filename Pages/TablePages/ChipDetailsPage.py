from Utilites.UIUtils import UIUtils
import time

class ChipDetails:
    def __init__(self, page, feature_name):
        self.page = page
        self.feature_name = feature_name
        self.ui_utils = UIUtils(page)
        self.table_locator = "table.table-chip-details"
        self.chip_details = self.page.get_by_role("menuitem", name="Chip Details")
        self.table_dashboard = self.page.get_by_role('button', name='Table Dashboard')

    def extract_chip_details_table(self):
        """
        Extracts chip details from the chip details table and returns a list of dicts.
        Each dict represents a chip row with keys as column headers.
        """
        self.ui_utils.click_to_element(self.table_dashboard)
        self.ui_utils.click_to_element(self.chip_details)
        time.sleep(4)
        table = self.page.locator(self.table_locator)
        headers = [h.strip() for h in table.locator("thead tr th").all_text_contents()]
        data = []
        rows = table.locator("tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td")
            row_data = {}
            for j in range(cells.count()):
                cell_texts = [t.strip() for t in cells.nth(j).locator(".player-name").all_text_contents()]
                row_data[headers[j]] = cell_texts if len(cell_texts) > 1 else (cell_texts[0] if cell_texts else "")
            data.append(row_data)
        return data