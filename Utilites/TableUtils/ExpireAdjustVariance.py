import requests
import time
from Utilites.ExcelRead.ConfigRead import ConfigUtils
from Pages.TablePages.PlayerTab import PlayerTab
from Pages.TablePages.InventoryTab import InventoryTab
from Pages.TablePages.ViewTableTab import ViewTableTab
from Utilites.TableUtils.TableActions import TableActions
from Utilites.ExcelRead.ExcelReader import read_chip_ids_df

class ExpireAndAdjustVariance:
    def __init__(self, page, feature_name):
        self.page = page
        self.feature_name = feature_name
        self.config_utils = ConfigUtils()
        self.config_utils.set_feature_name(self.feature_name)
        self.table_ip = self.config_utils.get_tableIP()
        self.player_tab = PlayerTab(page)
        self.inventory_tab = InventoryTab(page)
        self.view_table_tab = ViewTableTab(page)
        self.table_actions = TableActions(page, feature_name)

    def expire_and_adjust(self):
        """Expires and adjusts chip variance.
        Author:
            Prasad Kamble
        """
        self.page.wait_for_timeout(2000)
        self.player_tab.table_dashboard_button().click()
        self.player_tab.table_controls_menu_item().click()
        self.player_tab.expire_chips_button().click()
        self.player_tab.confirm_button().click()
        self.player_tab.close_button().click()
        self.move_all_chips_to_tt(self.table_ip)
        self.page.wait_for_timeout(2000)
        self.table_actions.navigate_to_tab(self.inventory_tab.inventory_tab(), wait_time=2000)
        # self.inventory_tab.inventory_tab().click()
        self.inventory_tab.scan_button().click()
        self.page.wait_for_timeout(2000)
        api_url = f"https://{self.table_ip}:790/api/table/v1/tableInfo"
        # Step 1: Wait for isScanning to be False
        for attempt in range(20):
            resp = requests.get(api_url, verify=False)
            data = resp.json()
            is_scanning = data.get("chipTrayStatus", {}).get("isScanning")
            print(f"Attempt {attempt+1}: isScanning={is_scanning}")
            if not is_scanning:
                break
            time.sleep(2)
        else:
            print("Timeout waiting for isScanning to become False (first check).")
            return

        # Step 2: Click Adjust if enabled
        try:
            adjust_button = self.inventory_tab.adjust_button()
            adjust_button.wait_for(state="visible", timeout=10000)
            if adjust_button.is_enabled():
                adjust_button.click()
                print("'Adjust' button is clickable.")
                self.page.wait_for_timeout(2000)
                self.inventory_tab.select_reason_option().click()
                self.page.wait_for_timeout(500)
                self.inventory_tab.reason_others_option().wait_for(state="visible", timeout=3000)
                self.inventory_tab.reason_others_option().click()
                self.page.wait_for_timeout(1000)
                self.inventory_tab.confirm_button().click()
                self.table_actions.navigate_to_tab(self.view_table_tab.view_table_tab(), wait_time=2000)
            else:
                print("'Adjust' button is not clickable.")
                self.table_actions.navigate_to_tab(self.view_table_tab.view_table_tab(), wait_time=2000)
                return
        except Exception as e:
            print(f"Error interacting with Adjust button: {e}")
            return

        # Step 3: Wait for isScanning to be False again
        for attempt in range(20):
            resp = requests.get(api_url, verify=False)
            data = resp.json()
            is_scanning = data.get("chipTrayStatus", {}).get("isScanning")
            print(f"Attempt {attempt+1} (after Adjust): isScanning={is_scanning}")
            if not is_scanning:
                break
            time.sleep(2)
        else:
            print("Timeout waiting for isScanning to become False (after Adjust).")
            return

    def move_all_chips_to_tt(self, table_ip):
        """
        Moves all chips from the Excel file to antenna 'TT' in a single API call.
        Author:
                Prasad Kamble
        """
        chips_df = read_chip_ids_df()
        api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
        headers = {'Content-Type': 'application/json'}

        # Prepare the data payload for all chips
        data = []
        for _, row in chips_df.iterrows():
            chip_id = row['chipsID']
            data.append({
                "chipId": chip_id,
                "antennaName": "TT",
                "acquired": "true"
            })

        # Send one POST request with all chips
        try:
            resp = requests.post(api_url, headers=headers, json=data, verify=False)
            print(f"Move all chips to TT response: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Error moving all chips to TT: {e}")