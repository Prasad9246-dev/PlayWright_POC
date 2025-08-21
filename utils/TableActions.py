import requests
import time
from conftest import get_tableIP, setup
from pages.PlayerTab import PlayerTab
from pages.InventoryTab import InventoryTab
from pages.ViewTableTab import ViewTableTab
from utils.UIUtils import UIUtils

class TableActions:
    def get_api_url(self):
        table_ip = get_tableIP()
        return f"https://{table_ip}:790/api/table/v1/tableInfo"

    def __init__(self, page):
        self.page = page
        self.player_tab = PlayerTab(page)
        self.inventory_tab = InventoryTab(page)
        self.view_table_tab = ViewTableTab(page)  
        self.ui_utils = UIUtils(self.page)  

    def table_close(self):
        # If "Table is closed" is already present, skip closing
        if self.page.get_by_text("Table is closed").is_visible():
            print("Table is already closed. Skipping close operation.")
            return
        print("Closing table...")
        self.player_tab.dropdown_button().click()
        self.player_tab.menu_item_close().click()
        self.player_tab.confirm_button().click()
        self.page.wait_for_timeout(4000)
        print("Table closed successfully.")

    def table_open(self):
        if self.page.get_by_text("Table is closed").is_visible():
            print("Opening table...")
            self.player_tab.dropdown_button().click()
            self.player_tab.menu_item_open().click()
            self.player_tab.confirm_button().click()
            self.page.wait_for_timeout(4000)
            print("Table opened successfully.")
        else:
            print("Table is already open. Skipping open operation.")

    def table_close_and_open(self):
        self.player_tab.PLAYERS_TAB.click
        self.table_close()
        self.table_open()

    def navigate_to_tab(self, tab_selector, wait_time=5000):
        """
        Navigates to a tab using the provided selector and waits for the specified time (ms).
        Example: navigate_to_tab(self.view_table_tab.view_table_tab())
        """
        try:
            tab = tab_selector
            tab.wait_for(state="visible", timeout=10000)
            for i in range(10):
                if tab.is_enabled():
                    break
                self.page.wait_for_timeout(500)
            tab.click()
            tab_name = self.ui_utils.get_text(tab_selector)
            print(f"Clicked tab: {tab_name if tab_name else tab_selector}")
            self.page.wait_for_timeout(wait_time)
        except Exception as e:
            print(f"[ERROR] Error clicking tab: {e}")
    
    def move_chips_between_antennas(self,table_ip, from_antenna, to_antenna, chip_ids: str):
        """
        Moves one or more chips from one antenna to another using the chipMove API.
        :param from_antenna: The antenna name to move FROM (string)
        :param to_antenna: The antenna name to move TO (string)
        :param chip_ids: A single chip ID or multiple chip IDs (comma separated string)
        """
        api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
        headers = {'Content-Type': 'application/json'}

        # # Split chip_ids by comma and strip whitespace
        # chip_id_list = [chip_id.strip() for chip_id in chip_ids.split(",")]

         # Accept comma-separated string or list
        if isinstance(chip_ids, str):
            chip_id_list = [chip_id.strip() for chip_id in chip_ids.split(",")]
        elif isinstance(chip_ids, list):
            chip_id_list = chip_ids
        else:
            raise ValueError("chip_ids must be a string or a list")

        # Remove chips from from_antenna
        data_remove = [{
            "chipId": chip_id,
            "antennaName": from_antenna,
            "acquired": "false"
        } for chip_id in chip_id_list]
        resp_remove = requests.post(api_url, headers=headers, json=data_remove, verify=False)
        print(f"Remove chip(s) response: {resp_remove.status_code} {resp_remove.text}")

        # Place chips on to_antenna
        data_place = [{
            "chipId": chip_id,
            "antennaName": to_antenna,
            "acquired": "true"
        } for chip_id in chip_id_list]
        resp_place = requests.post(api_url, headers=headers, json=data_place, verify=False)
        print(f"Place chip(s) response: {resp_place.status_code} {resp_place.text}")
            
    def chip_move_antenna(self,table_ip, antenna_name: str, chip_ids, acquired: str):
        """
        Moves (sets acquired true/false) one or more chips on the specified antenna using the chipMove API.
        :param antenna_name: The antenna name to move the chip from (string)
        :param chip_ids: A single chip ID (string) or multiple chip IDs (comma-separated string or list)
        :param acquired: "true" to place, "false" to remove (string)
        """
        try:
            api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
            headers = {'Content-Type': 'application/json'}

            # Accept comma-separated string or list
            if isinstance(chip_ids, str):
                chip_id_list = [chip_id.strip() for chip_id in chip_ids.split(",")]
            else:
                chip_id_list = list(chip_ids)

            data = [{
                "chipId": chip_id,
                "antennaName": antenna_name,
                "acquired": acquired
            } for chip_id in chip_id_list]

            resp = requests.post(api_url, headers=headers, json=data, verify=False)
            print(f"Chip move on '{antenna_name}' (acquired={acquired}) response: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Error moving chip(s) on antenna '{antenna_name}': {e}")

    def get_chip_ids_for_denom(self,chips_df, denom):
        """
        Returns a list of chip IDs from chips_df that sum up to the requested denom.
        Prefers exact match, otherwise combines smaller chips.
        Removes used chips from chips_df.
        """
        denom = int(denom)
        chips_df["Denom"] = chips_df["Denom"].astype(int)
        chip_ids = []

        # Try exact match first
        exact = chips_df[chips_df["Denom"] == denom]
        if not exact.empty:
            chip_id = exact.iloc[0]["chipsID"]
            chip_ids.append(chip_id)
            chips_df.drop(exact.index[0], inplace=True)
            return chip_ids

        # Try to combine smaller chips
        sorted_chips = chips_df.sort_values(by="Denom", ascending=False)
        total = 0
        used_indices = []
        for idx, row in sorted_chips.iterrows():
            if total + row["Denom"] <= denom:
                chip_ids.append(row["chipsID"])
                total += row["Denom"]
                used_indices.append(idx)
                if total == denom:
                    break

        # Remove used chips from chips_df
        chips_df.drop(used_indices, inplace=True)

        if total == denom:
            return chip_ids
        else:
            print(f"Cannot fulfill denom {denom} with available chips.")
            return []

    def get_n_chips_for_denom(self,chips_df, denom_and_count):
        """
        Returns a list of N chip IDs for the given denom from chips_df.
        Example: denom_and_count = "100-5" returns 5 chips of denom 100.
        Removes used chips from chips_df.
        """
        try:
            denom_str, count_str = denom_and_count.split('-')
            denom = int(denom_str)
            count = int(count_str)
        except Exception:
            print(f"Invalid format: {denom_and_count}. Use 'denom-count', e.g., '100-5'.")
            return []

        chips_df["Denom"] = chips_df["Denom"].astype(int)
        matching_chips = chips_df[chips_df["Denom"] == denom]
        if len(matching_chips) < count:
            print(f"Not enough chips of denom {denom}. Requested: {count}, Available: {len(matching_chips)}")
            chip_ids = matching_chips["chipsID"].tolist()
            chips_df.drop(matching_chips.index, inplace=True)
            return chip_ids  # Return as many as available
        else:
            chip_ids = matching_chips.iloc[:count]["chipsID"].tolist()
            chips_df.drop(matching_chips.iloc[:count].index, inplace=True)
            return chip_ids

    def transfer_from_view_table(self):
        """
        Clicks the (0) button, selects 'Transfer', confirms, and clicks the 'Transfer' text
        using selectors from ViewTableTab only.
        """
        try:
            self.view_table_tab.BuyIn_GreenBar.click()
            self.view_table_tab.Transfer.click()
            # Check if the 'Transfer' header exists instead of clicking it
            if self.view_table_tab.transfer_Header.is_visible():
                print("Transfer header is visible. Transfer dialog opened successfully.")
            else:
                print("[ERROR] Transfer header is not visible.")
            self.view_table_tab.transfer_ConfirmButton.click()
            print("Transfer from View Table completed.")
        except Exception as e:
            print(f"[ERROR] Transfer from View Table failed: {e}")

    def change_transaction_from_view_table(self, table_ip, chips_df):
        """
        Clicks the (0) button, selects 'Change Transaction', confirms, and checks if the 'Change Transaction' header exists
        using selectors from ViewTableTab only.
        """
        try:
            first_chip_ids = self.get_chip_ids_for_denom(chips_df, 500)  # Example: get $500 chips for change
            print(first_chip_ids)
            self.move_chips_between_antennas(table_ip, "TT", "DEALER", first_chip_ids)
            self.view_table_tab.BuyIn_Close.click()
            time.sleep(2)
            self.page.reload()
            try:
                # Wait for any overlay to disappear
                self.page.wait_for_selector("app-dealer-info", state="hidden", timeout=10000)
                button = self.page.locator('#dealerAndAggrAmount')
                button.wait_for(state="visible", timeout=5000)
                button.scroll_into_view_if_needed()
                button.click()
                print("Clicked Dealer and Aggregate Amount button.")
            except Exception as e:
                print(f"[ERROR] Could not click Dealer and Aggregate Amount button: {e}")
            #self.view_table_tab.dealer_and_aggr_amount_button.click()
            time.sleep(2)
            self.view_table_tab.Change.click()
            time.sleep(3)
            # Check if the 'Change Transaction' header exists instead of clicking it
            if self.view_table_tab.Change_Header.is_visible():
                print("Change Transaction header is visible. Change Transaction dialog opened successfully.")
                second_chip_ids = self.get_n_chips_for_denom(chips_df, "100-5")  # Example: get 5 chips of $100
                print(second_chip_ids)
               # self.move_chips_between_antennas(table_ip, "TT", "DEALER", first_chip_ids)
                self.move_chips_between_antennas(table_ip, "TT", "DEALER", second_chip_ids)
                self.view_table_tab.Change_ConfirmButton.click()
                print("Change Transaction from View Table completed.")
            else:
                print("[ERROR] Change Transaction header is not visible.")
        except Exception as e:
            print(f"[ERROR] Change Transaction from View Table failed: {e}")

    def move_to_sessions_tab(self):
        """
        Navigates to the Sessions tab using the selector from ViewTableTab.
        """
        try:
            self.view_table_tab.SessionsTab.wait_for(state="visible", timeout=10000)
            self.view_table_tab.SessionsTab.click()
            print("Moved to Sessions tab.")
            self.page.wait_for_timeout(3000)
        except Exception as e:
            print(f"[ERROR] Could not move to Sessions tab: {e}")

    def check_chip_in_value(self, expected_value="1000"):
        """
        Navigates to the Sessions tab, clicks the first row, checks if the chip in value is correct,
        clicks on the chip in value, and verifies the 'Update Chips In' header is visible.
        """
        try:
            # Move to Sessions tab
            self.move_to_sessions_tab()
            self.page.wait_for_timeout(2000)

            # Click on the first row in the Sessions table
            first_cell = self.page.locator("table[role='table'] tbody tr[role='row']").nth(0).locator("td").nth(0)
            time.sleep(2)
            first_cell.click()
            print("Clicked on first row in Sessions tab.")

            # Check if the chip in value is correct (1000)
            time.sleep(4)
            chip_in_locator = self.page.locator(f'span.wd-flex.session-summary__value.label-underline', has_text=expected_value)
            if chip_in_locator.is_visible():
                print(f"Chip In value '{expected_value}' is visible.")
                chip_in_locator.nth(0).click()  # Click the first occurrence of the chip in value
            else:
                print(f"[ERROR] Chip In value '{expected_value}' is not visible.")
                return

        except Exception as e:
            print(f"[ERROR] Check ChipIn Value failed: {e}")





