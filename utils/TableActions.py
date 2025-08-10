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

        # Split chip_ids by comma and strip whitespace
        chip_id_list = [chip_id.strip() for chip_id in chip_ids.split(",")]

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

