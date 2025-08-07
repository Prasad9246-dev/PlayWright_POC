import requests
import time
from conftest import get_tableIP
from pages.PlayerTab import PlayerTab
from pages.InventoryTab import InventoryTab
from pages.ViewTableTab import ViewTableTab
from utils.TableActions import TableActions

class ExpireAndAdjustVariance:
    def __init__(self, page):
        self.page = page
        self.player_tab = PlayerTab(page)
        self.inventory_tab = InventoryTab(page)
        self.view_table_tab = ViewTableTab(page)
        self.table_actions = TableActions(page)

    def expire_and_adjust(self):
        self.table_actions.chip_move_from_antenna(antenna_name="TT", chip_id="e00540011226b05d", acquired="true")
        self.page.wait_for_timeout(2000)
        self.player_tab.table_dashboard_button().click()
        self.player_tab.table_controls_menu_item().click()
        self.player_tab.expire_chips_button().click()
        self.player_tab.confirm_button().click()
        self.player_tab.close_button().click()
        self.inventory_tab.inventory_tab().click()
        self.inventory_tab.scan_button().click()
        self.page.wait_for_timeout(2000)
        api_url = f"https://{get_tableIP()}:790/api/table/v1/tableInfo"
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
                self.table_actions.navigate_to_tab('View Table', wait_time=2000)
            else:
                print("'Adjust' button is not clickable.")
                self.table_actions.navigate_to_tab('View Table', wait_time=2000)
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

