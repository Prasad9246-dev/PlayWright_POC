import requests
import time
from Utilites.ExcelRead.ConfigRead import ConfigUtils
from Pages.TablePages.PlayerTab import PlayerTab
from Pages.TablePages.InventoryTab import InventoryTab
from Pages.TablePages.ViewTableTab import ViewTableTab
from Utilites.TableUtils.TableActions import TableActions
from Utilites.ExcelRead.ExcelReader import read_chip_ids_df
from Utilites.Logs.LoggerUtils import LoggerUtils
from Utilites.UIUtils import UIUtils

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
        self.ui_utils = UIUtils(self.page)
        self.table_actions = TableActions(page, feature_name)
        self.logger_utils = LoggerUtils(self.feature_name)

    def expire_and_adjust(self):
        """Expires and adjusts chip variance.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log("Starting expire_and_adjust process.")
        self.page.wait_for_timeout(2000)
        self.ui_utils.click_to_element(self.player_tab.table_dashboard_button())
        self.logger_utils.log("Clicked table dashboard button.")
        self.ui_utils.click_to_element(self.player_tab.table_controls_menu_item())
        self.logger_utils.log("Clicked table controls menu item.")
        self.ui_utils.click_to_element(self.player_tab.expire_chips_button())
        self.logger_utils.log("Clicked expire chips button.")
        self.ui_utils.click_to_element(self.player_tab.confirm_button())
        self.logger_utils.log("Clicked confirm button for expire chips.")
        self.ui_utils.click_to_element(self.player_tab.close_button())
        self.logger_utils.log("Clicked close button after expire chips.")
        self.move_all_chips_to_tt(self.table_ip)
        self.logger_utils.log("Moved all chips to TT antenna.")
        self.page.wait_for_timeout(2000)
        self.table_actions.navigate_to_tab(self.inventory_tab.inventory_tab(), wait_time=2000)
        self.logger_utils.log("Navigated to Inventory tab.")
        self.ui_utils.click_to_element(self.inventory_tab.scan_button())
        self.logger_utils.log("Clicked scan button.")
        self.page.wait_for_timeout(2000)
        api_url = f"https://{self.table_ip}:790/api/table/v1/tableInfo"
        # Step 1: Wait for isScanning to be False
        for attempt in range(20):
            resp = requests.get(api_url, verify=False)
            data = resp.json()
            is_scanning = data.get("chipTrayStatus", {}).get("isScanning")
            self.logger_utils.log(f"Attempt {attempt+1}: isScanning={is_scanning}")
            print(f"Attempt {attempt+1}: isScanning={is_scanning}")
            if not is_scanning:
                break
            time.sleep(2)
        else:
            msg = "Timeout waiting for isScanning to become False (first check)."
            self.logger_utils.log(msg)
            print(msg)
            return

        # Step 2: Click Adjust if enabled
        try:
            adjust_button = self.inventory_tab.adjust_button()
            adjust_button.wait_for(state="visible", timeout=10000)
            if adjust_button.is_enabled():
                adjust_button.click()
                self.logger_utils.log("'Adjust' button is clickable.")
                print("'Adjust' button is clickable.")
                self.page.wait_for_timeout(2000)
                self.ui_utils.click_to_element(self.inventory_tab.select_reason_option())
                self.logger_utils.log("Selected reason option.")
                self.page.wait_for_timeout(500)
                self.inventory_tab.reason_others_option().wait_for(state="visible", timeout=3000)
                self.ui_utils.click_to_element(self.inventory_tab.reason_others_option())
                self.logger_utils.log("Selected 'Others' reason option.")
                self.page.wait_for_timeout(1000)
                self.ui_utils.click_to_element(self.inventory_tab.confirm_button())
                self.logger_utils.log("Clicked confirm button for adjust.")
                self.table_actions.navigate_to_tab(self.view_table_tab.view_table_tab(), wait_time=2000)
                self.logger_utils.log("Navigated to View Table tab after adjust.")
            else:
                msg = "'Adjust' button is not clickable."
                self.logger_utils.log(msg)
                print(msg)
                self.table_actions.navigate_to_tab(self.view_table_tab.view_table_tab(), wait_time=2000)
                self.logger_utils.log("Navigated to View Table tab because adjust button was not clickable.")
                return
        except Exception as e:
            msg = f"Error interacting with Adjust button: {e}"
            self.logger_utils.log(msg)
            print(msg)
            return

        # Step 3: Wait for isScanning to be False again
        for attempt in range(20):
            resp = requests.get(api_url, verify=False)
            data = resp.json()
            is_scanning = data.get("chipTrayStatus", {}).get("isScanning")
            self.logger_utils.log(f"Attempt {attempt+1} (after Adjust): isScanning={is_scanning}")
            print(f"Attempt {attempt+1} (after Adjust): isScanning={is_scanning}")
            if not is_scanning:
                break
            time.sleep(2)
        else:
            msg = "Timeout waiting for isScanning to become False (after Adjust)."
            self.logger_utils.log(msg)
            print(msg)
            return
        self.logger_utils.log("expire_and_adjust process completed successfully.")

    def move_all_chips_to_tt(self, table_ip):
        """
        Moves all chips from the Excel file to antenna 'TT' in a single API call.
        Author:
                Prasad Kamble
        """
        self.logger_utils.log("Starting move_all_chips_to_tt process.")
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

        self.logger_utils.log(f"Prepared payload for {len(data)} chips to move to TT antenna.")
        # Send one POST request with all chips
        try:
            resp = requests.post(api_url, headers=headers, json=data, verify=False)
            self.logger_utils.log(f"Move all chips to TT response: {resp.status_code} {resp.text}")
            print(f"Move all chips to TT response: {resp.status_code} {resp.text}")
        except Exception as e:
            self.logger_utils.log(f"[ERROR] Error moving all chips to TT: {e}")
            print(f"Error moving all chips to TT: {e}")