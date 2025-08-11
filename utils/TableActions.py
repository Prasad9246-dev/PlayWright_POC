import requests
import time
from conftest import get_tableIP, setup
from pages.PlayerTab import PlayerTab
from pages.InventoryTab import InventoryTab
from pages.ViewTableTab import ViewTableTab

class TableActions:
    def get_api_url(self):
        table_ip = get_tableIP()
        return f"https://{table_ip}:790/api/table/v1/tableInfo"

    def __init__(self, page):
        self.page = page
        self.player_tab = PlayerTab(page)
        self.inventory_tab = InventoryTab(page)
        self.view_table_tab = ViewTableTab(page)    

    def table_close(self):
        self.player_tab.dropdown_button().click()
        self.player_tab.menu_item_close().click()
        self.player_tab.confirm_button().click()
        self.page.wait_for_timeout(4000)

    def table_open(self):
        self.player_tab.dropdown_button().click()
        self.player_tab.menu_item_open().click()
        self.player_tab.confirm_button().click()
        self.page.wait_for_timeout(4000)

    def table_close_and_open(self):
        self.table_close()
        self.table_open()

    def expire_and_adjust(self):
        self.player_tab.table_dashboard_button().click()
        self.player_tab.table_controls_menu_item().click()
        self.player_tab.expire_chips_button().click()
        self.player_tab.confirm_button().click()
        self.player_tab.close_button().click()
        self.inventory_tab.inventory_tab().click()
        self.inventory_tab.scan_button().click()
        self.page.wait_for_timeout(2000)
        api_url = self.get_api_url()
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
                self.page.wait_for_timeout(500)  # Give time for overlay to appear
                self.inventory_tab.reason_others_option().wait_for(state="visible", timeout=3000)
                self.inventory_tab.reason_others_option().click()
                self.page.wait_for_timeout(1000)
                self.inventory_tab.confirm_button().click()
            else:
                print("'Adjust' button is not clickable.")
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


    def navigate_to_tab(self, tab_name, wait_time=5000):
        """
        Navigates to a tab by its accessible name and waits for the specified time (ms).
        Example: navigate_to_tab('View Table')
        """
        try:
            tab = self.page.get_by_role('tab', name=tab_name)
            tab.wait_for(state="visible", timeout=10000)
            for i in range(10):
                if tab.is_enabled():
                    break
                self.page.wait_for_timeout(500)
            tab.click()
            print(f"Clicked '{tab_name}' tab.")
            self.page.wait_for_timeout(wait_time)
        except Exception as e:
            print(f"Error clicking '{tab_name}' tab: {e}")
            
            
    def remove_chip_from_antenna(self, antenna_name: str, chip_id: str):
        """
        Removes (falses) the chip from the specified antenna using the chipMove API.
        :param antenna_name: The antenna name to remove the chip from (string)
        :param chip_id: The chip's unique ID (string)
        """
        try:
            table_ip = get_tableIP()
            api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
            headers = {'Content-Type': 'application/json'}
            data_remove = [{
                "chipId": chip_id,
                "antennaName": antenna_name,
                "acquired": "false"
            }]
            resp_remove = requests.post(api_url, headers=headers, json=data_remove, verify=False)
            print(f"Remove chip from '{antenna_name}' response: {resp_remove.status_code} {resp_remove.text}")
        except Exception as e:
            print(f"Error removing chip from antenna '{antenna_name}': {e}")

    
    def move_chip(self, from_antenna, to_antenna, chip_id="e00540011226b05d"):
        """
        Moves a chip from one antenna to another using the chipMove API.
        :param from_antenna: The antenna name to move FROM (string)
        :param to_antenna: The antenna name to move TO (string)
        :param chip_id: The chip's unique ID (string), default is example value
        """
        table_ip = get_tableIP()
        api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
        headers = {'Content-Type': 'application/json'}

        # Step 1: Remove chip from from_antenna (acquired: false)
        data_remove = [{
            "chipId": chip_id,
            "antennaName": from_antenna,
            "acquired": "false"
        }]
        resp_remove = requests.post(api_url, headers=headers, json=data_remove, verify=False)
        print(f"Remove chip response: {resp_remove.status_code} {resp_remove.text}")

        # Step 2: Place chip on to_antenna (acquired: true)
        data_place = [{
            "chipId": chip_id,
            "antennaName": to_antenna,
            "acquired": "true"
        }]
        resp_place = requests.post(api_url, headers=headers, json=data_place, verify=False)
        print(f"Place chip response: {resp_place.status_code} {resp_place.text}")

    def buy_in(self, player_id: str, seat_number: int, chip_id: str, buyin_type: str):
        """
        Moves chip to DEALER, then automates the Buy-In process for a given player, seat, and chip.
        Supports Rated, Known, and Anonymous buy-ins.
        Calls move_chip to place the chip on the seat's antenna after buy-in.
        :param player_id: The player ID as string (e.g., "6001")
        :param seat_number: The seat number as integer (e.g., 1)
        :param chip_id: The chip's unique ID as string
        :param buyin_type: "rated", "known", or "anonymous"
        """
        try:
            # Step 1: Move chip from TT to DEALER
            self.move_chip("TT", "DEALER", chip_id)
            self.page.wait_for_timeout(1000)

            # Step 2: Buy-In UI process

            if buyin_type.lower() == "rated":
                # Rated buy-in (existing logic)
                self.view_table_tab.seat_section(seat_number).click()
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().fill(player_id)
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().press('Enter')
                self.page.wait_for_timeout(1000)
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Rated Buy-In process completed for seat {seat_number} and player {player_id}.")

            elif buyin_type.lower() == "known":
                # Known buy-in (example: select from known list, or similar logic)
                self.view_table_tab.player_search_box().fill(player_id)
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().press('Enter')
                self.page.wait_for_timeout(1000)
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Known Buy-In process completed for seat {seat_number} and player {player_id}.")

            elif buyin_type.lower() == "anonymous":
                # Anonymous buy-in (example: click anonymous button, skip player_id)
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Anonymous Buy-In process completed for seat {seat_number}.")

            else:
                print(f"Unknown buyin_type '{buyin_type}' specified.")
                return

            # Step 3: Move chip from DEALER to the seat's antenna (assuming antenna name is based on seat number)
            self.remove_chip_from_antenna("DEALER", chip_id)
            self.page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Error during Buy-In: {e}")

    def chip_move_from_antenna(self, antenna_name: str, chip_id: str, acquired: str = "false"):
        """
        Moves (sets acquired true/false) the chip on the specified antenna using the chipMove API.
        :param antenna_name: The antenna name to move the chip from (string)
        :param chip_id: The chip's unique ID (string)
        :param acquired: "true" to place, "false" to remove (string)
        """
        try:
            table_ip = get_tableIP()
            api_url = f"https://{table_ip}:790/api/table/v1/chipMove"
            headers = {'Content-Type': 'application/json'}
            data = [{
                "chipId": chip_id,
                "antennaName": antenna_name,
                "acquired": acquired
            }]
            resp = requests.post(api_url, headers=headers, json=data, verify=False)
            print(f"Chip move on '{antenna_name}' (acquired={acquired}) response: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Error moving chip on antenna '{antenna_name}': {e}")

    def draw_cards(self, table_ip: str, *cards):
        """
        Draws one or more cards on the table using the drawcard API (GET method).
        After all cards are drawn, hits the shoebutton API.
        :param table_ip: The table IP address as a string.
        :param cards: Variable number of card strings (e.g., "4s", "5h", "6d").
        """
        api_url = f"https://{table_ip}:790/api/table/v1/drawcard"
        headers = {'Content-Type': 'application/json'}
        for card in cards:
            try:
                url_with_param = f"{api_url}?card={card}"
                resp = requests.get(url_with_param, headers=headers, verify=False)
                print(f"Draw card '{card}' response: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"Error drawing card '{card}': {e}")
        # After all cards are drawn, hit the shoebutton API
        try:
            shoe_url = f"https://{table_ip}:790/api/table/v1/shoebutton"
            resp_shoe = requests.get(shoe_url, headers=headers, verify=False)
            print(f"Shoe button API response: {resp_shoe.status_code} {resp_shoe.text}")
        except Exception as e:
            print(f"Error calling shoe button API: {e}")

