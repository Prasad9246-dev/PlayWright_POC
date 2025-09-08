import re
import time
import requests
from Utilites.ExcelRead.ConfigRead import ConfigUtils
from Pages.TablePages.PlayerTab import PlayerTab
from Pages.TablePages.InventoryTab import InventoryTab
from Pages.TablePages.ViewTableTab import ViewTableTab
from Utilites.UIUtils import UIUtils
from Utilites.Logs.LoggerUtils import LoggerUtils

class TableActions:
    def __init__(self, page, feature_name):
        from Pages.TablePages.SessionsTab import SessionsTab
        self.page = page
        self.feature_name = feature_name
        self.config_utils = ConfigUtils()
        self.config_utils.set_feature_name(self.feature_name)
        self.player_tab = PlayerTab(page)
        self.inventory_tab = InventoryTab(page)
        self.view_table_tab = ViewTableTab(page)  
        self.sessions_tab = SessionsTab(page, self.feature_name, self)
        self.ui_utils = UIUtils(self.page)
        self.logger_utils = LoggerUtils(self.feature_name)

    def get_api_url(self):
        """
        Constructs the API URL for table information.
        Author:
            Prasad Kamble
        """
        table_ip = self.config_utils.get_tableIP()
        api_url = f"https://{table_ip}:790/api/table/v1/tableInfo"
        self.logger_utils.log(f"Constructed API URL: {api_url}")
        return api_url

    def table_close(self):
        """
        Closes the table if it is open.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log("Attempting to close the table.")
        self.page.wait_for_timeout(3000)
        if self.page.get_by_text("Table is closed").is_visible():
            self.logger_utils.log("Table is already closed. Skipping close operation.")
            print("Table is already closed. Skipping close operation.")
            return
        print("Closing table...")
        self.logger_utils.log("Closing table...")
        self.player_tab.dropdown_button().click()
        self.player_tab.menu_item_close().click()
        self.player_tab.confirm_button().click()
        self.page.wait_for_timeout(4000)
        self.logger_utils.log("Table closed successfully.")
        print("Table closed successfully.")

    def table_open(self):
        """
        Opens the table if it is closed.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log("Attempting to open the table.")
        self.page.wait_for_timeout(3000)
        if self.page.get_by_text("Table is closed").is_visible():
            print("Opening table...")
            self.player_tab.dropdown_button().click()
            self.player_tab.menu_item_open().click()
            self.player_tab.confirm_button().click()
            self.page.wait_for_timeout(4000)
            self.logger_utils.log("Table opened successfully.")
            print("Table opened successfully.")
        else:
            self.logger_utils.log("Table is already open. Skipping open operation.")
            print("Table is already open. Skipping open operation.")

    def table_close_and_open(self):
        """
        Closes and reopens the table.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log("Starting table close and open sequence.")
        self.navigate_to_tab(self.player_tab.Players_TAB)
        self.table_close()
        self.table_open()
        self.logger_utils.log("Completed table close and open sequence.")

    def navigate_to_tab(self, tab_selector, wait_time=5000):
        """
        Navigates to a tab using the provided selector and waits for the specified time (ms).
        Example: navigate_to_tab(self.view_table_tab.view_table_tab())
        Author:
            Prasad Kamble
        """
        try:
            self.logger_utils.log(f"Navigating to tab: {tab_selector}")
            tab = tab_selector
            tab.wait_for(state="visible", timeout=10000)
            for i in range(10):
                if tab.is_enabled():
                    break
                self.page.wait_for_timeout(500)
            tab.click()
            tab_name = self.ui_utils.get_text(tab_selector)
            self.logger_utils.log(f"Clicked tab: {tab_name if tab_name else tab_selector}")
            print(f"Clicked tab: {tab_name if tab_name else tab_selector}")
            self.page.wait_for_timeout(wait_time)
        except Exception as e:
            self.logger_utils.log(f"[ERROR] Error clicking tab: {e}")
            print(f"[ERROR] Error clicking tab: {e}")
    
    def move_chips_between_antennas(self,table_ip, from_antenna, to_antenna, chip_ids: str):
        """
        Moves one or more chips from one antenna to another using the chipMove API.
        :param from_antenna: The antenna name to move FROM (string)
        :param to_antenna: The antenna name to move TO (string)
        :param chip_ids: A single chip ID or multiple chip IDs (comma separated string)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(
        f"Starting move_chips_between_antennas: from '{from_antenna}' to '{to_antenna}' with chip_ids '{chip_ids}'"
        )
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
        self.logger_utils.log(
        f"Remove chip(s) response: {resp_remove.status_code} {resp_remove.text}"
        )
        print(f"Remove chip(s) response: {resp_remove.status_code} {resp_remove.text}")

        # Place chips on to_antenna
        data_place = [{
            "chipId": chip_id,
            "antennaName": to_antenna,
            "acquired": "true"
        } for chip_id in chip_id_list]
        resp_place = requests.post(api_url, headers=headers, json=data_place, verify=False)
        self.logger_utils.log(
        f"Place chip(s) response: {resp_place.status_code} {resp_place.text}"
        )
        print(f"Place chip(s) response: {resp_place.status_code} {resp_place.text}")
        self.logger_utils.log(
        f"Completed move_chips_between_antennas: from '{from_antenna}' to '{to_antenna}' with chip_ids '{chip_ids}'"
        )
            
    def chip_move_antenna(self,table_ip, antenna_name: str, chip_ids, acquired: str):
        """
        Moves (sets acquired true/false) one or more chips on the specified antenna using the chipMove API.
        :param antenna_name: The antenna name to move the chip from (string)
        :param chip_ids: A single chip ID (string) or multiple chip IDs (comma-separated string or list)
        :param acquired: "true" to place, "false" to remove (string)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(
        f"Starting chip_move_antenna: antenna='{antenna_name}', acquired='{acquired}', chip_ids='{chip_ids}'"
        )
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
            self.logger_utils.log(
            f"Chip move on '{antenna_name}' (acquired={acquired}) response: {resp.status_code} {resp.text}"
            )
            print(f"Chip move on '{antenna_name}' (acquired={acquired}) response: {resp.status_code} {resp.text}")
        except Exception as e:
            self.logger_utils.log(
            f"[ERROR] Error moving chip(s) on antenna '{antenna_name}': {e}"
            )
            print(f"Error moving chip(s) on antenna '{antenna_name}': {e}")

    def get_chip_ids_for_denom(self,chips_df, denom):
        """
        Returns a list of chip IDs from chips_df that sum up to the requested denom.
        Prefers exact match, otherwise combines smaller chips.
        Removes used chips from chips_df.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Getting chip IDs for denom: {denom}")
        denom = int(denom)
        chips_df["Denom"] = chips_df["Denom"].astype(int)
        chip_ids = []

        # Try exact match first
        exact = chips_df[chips_df["Denom"] == denom]
        if not exact.empty:
            chip_id = exact.iloc[0]["chipsID"]
            chip_ids.append(chip_id)
            chips_df.drop(exact.index[0], inplace=True)
            self.logger_utils.log(f"Found exact match for denom {denom}: {chip_id}")
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
            self.logger_utils.log(f"Combined chips for denom {denom}: {chip_ids}")
            return chip_ids
        else:
            msg = f"Cannot fulfill denom {denom} with available chips."
            self.logger_utils.log(msg)
            print(msg)
            return []

    def get_n_chips_for_denom(self,chips_df, denom_and_count):
        """
        Returns a list of N chip IDs for the given denom from chips_df.
        Example: denom_and_count = "100-5" returns 5 chips of denom 100.
        Removes used chips from chips_df.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Getting chips for: {denom_and_count}")
        try:
            denom_str, count_str = denom_and_count.split('-')
            denom = int(denom_str)
            count = int(count_str)
        except Exception:
            msg = f"Invalid format: {denom_and_count}. Use 'denom-count', e.g., '100-5'."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return []

        chips_df["Denom"] = chips_df["Denom"].astype(int)
        matching_chips = chips_df[chips_df["Denom"] == denom]
        if len(matching_chips) < count:
            msg = f"Not enough chips of denom {denom}. Requested: {count}, Available: {len(matching_chips)}"
            self.logger_utils.log(f"[WARN] {msg}")
            print(msg)
            chip_ids = matching_chips["chipsID"].tolist()
            chips_df.drop(matching_chips.index, inplace=True)
            return chip_ids  # Return as many as available
        else:
            chip_ids = matching_chips.iloc[:count]["chipsID"].tolist()
            chips_df.drop(matching_chips.iloc[:count].index, inplace=True)
            self.logger_utils.log(f"Returning chip IDs for denom {denom}: {chip_ids}")
            return chip_ids

    def clock_in_player(self, tab_name, seat_num, player_id):
        """
        Navigates to the given tab, selects the player card by seat number, enters the player ID,
        clicks the first row/first column cell, and clicks the clock-in player button.
        Handles Players_TAB and View_Table_TAB, else prints error.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Attempting to clock in player_id={player_id} at seat_num={seat_num} on tab={tab_name}.")
        if tab_name == "Players_TAB":
            self.logger_utils.log("Navigating to Players_TAB for clock-in.")
            self.navigate_to_tab(self.player_tab.Players_TAB)
            self.logger_utils.log(f"Clicking player card at seat {seat_num}.")
            self.ui_utils.click_to_element(self.player_tab.player_card_position(seat_num))
            self.logger_utils.log(f"Filling player ID: {player_id}.")
            self.ui_utils.fill_element(self.player_tab.Enter_Player_ID, player_id)
            self.logger_utils.log("Pressing enter after filling player ID.")
            self.ui_utils.press_enter(self.player_tab.Enter_Player_ID)
            self.logger_utils.log("Clicking first row, first column selector.")
            self.ui_utils.click_to_element(self.player_tab.first_row_first_col_selector)
            self.logger_utils.log("Clicking clock-in player button.")
            self.ui_utils.click_to_element(self.player_tab.clock_in_player_button)
            self.logger_utils.log(f"Clocked in player_id={player_id} at seat_num={seat_num} on Players_TAB.")
        elif tab_name == "View_Table_TAB":
            self.logger_utils.log("Navigating to View_Table_TAB for clock-in.")
            self.navigate_to_tab(self.view_table_tab.view_table_tab())
            self.logger_utils.log(f"Clicking clock-in seat number {seat_num}.")
            self.ui_utils.click_to_element(self.view_table_tab.clockin_seat_num(seat_num))
            self.logger_utils.log(f"Filling player ID: {player_id}.")
            self.ui_utils.fill_element(self.view_table_tab.player_id_input, player_id)
            self.logger_utils.log("Pressing enter after filling player ID.")
            self.ui_utils.press_enter(self.view_table_tab.player_id_input)
            self.logger_utils.log("Clicking clock-in button.")
            self.ui_utils.click_to_element(self.view_table_tab.clock_in_button)
            self.logger_utils.log(f"Clocked in player_id={player_id} at seat_num={seat_num} on View_Table_TAB.")
        else:
            msg = f"Tab name '{tab_name}' is incorrect. Supported: 'Players_TAB', 'View_Table_TAB'."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            
    def clock_out_player(self, seat_num):
        """
        Navigates to the Players tab, clicks the dot button for the given seat number,
        then clicks the clock-out and clock-out close buttons.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Attempting to clock out player at seat_num={seat_num}.")
        self.navigate_to_tab(self.player_tab.Players_TAB)
        self.logger_utils.log(f"Clicking dot button for seat {seat_num}.")
        self.ui_utils.click_to_element(self.player_tab.player_card_dot(seat_num))
        self.logger_utils.log("Clicking clock-out button.")
        self.ui_utils.click_to_element(self.player_tab.clock_out_button)
        self.logger_utils.log("Clicking clock-out close button.")
        self.ui_utils.click_to_element(self.player_tab.clock_out_close_button)
        self.logger_utils.log(f"Clocked out player at seat_num={seat_num}.")
    
    def submit_manual_rating(self, player_id, tab_name, seat_num, buyin, average_bet, casino_win_loss, mid=None):
        """
        Submits a manual rating for a player on Players tab or Sessions tab.
        Args:
            player_id: Player ID to enter
            tab_name: 'Players_TAB' or 'Sessions_TAB'
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        """
        self.logger_utils.log(
            f"Submitting manual rating for player_id={player_id}, tab_name={tab_name}, seat_num={seat_num}, buyin={buyin}, average_bet={average_bet}, casino_win_loss={casino_win_loss}, mid={mid}"
        )
        if tab_name == "Sessions_TAB":
            self.submit_manual_rating_sessions_tab(player_id, seat_num, buyin, average_bet, casino_win_loss, mid)
        elif tab_name == "Players_TAB":
            self.submit_manual_rating_players_tab(player_id, seat_num, buyin, average_bet, casino_win_loss, mid)
        else:
            msg = f"Tab name '{tab_name}' is not supported. Use 'Players_TAB' or 'Sessions_TAB'."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
                     
    def save_manual_rating(self, player_id, tab_name, seat_num, buyin, average_bet, casino_win_loss, mid):
        """
        Submits a manual rating for a player on Players tab or Sessions tab.
        Args:
            player_id: Player ID to enter
            tab_name: 'Players_TAB' or 'Sessions_TAB'
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        """
        self.logger_utils.log(
            f"Saving manual rating for player_id={player_id}, tab_name={tab_name}, seat_num={seat_num}, buyin={buyin}, average_bet={average_bet}, casino_win_loss={casino_win_loss}, mid={mid}"
        )
        if tab_name == "Sessions_TAB":
            self.save_manual_rating_sessions_tab(player_id, seat_num, buyin, average_bet, casino_win_loss, mid)
        elif tab_name == "Players_TAB":
            self.save_manual_rating_players_tab(player_id, seat_num, buyin, average_bet, casino_win_loss, mid)
        else:
            msg = f"Tab name '{tab_name}' is not supported. Use 'Players_TAB' or 'Sessions_TAB'."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
    
    def submit_manual_rating_sessions_tab(self, player_id, seat_num, buyin, average_bet, casino_win_loss, mid=None):
        """
        Submits a manual rating for a player on Sessions tab.
        Args:
            player_id: Player ID to enter
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(
            f"Submitting manual rating (Sessions tab) for player_id={player_id}, seat_num={seat_num}, buyin={buyin}, average_bet={average_bet}, casino_win_loss={casino_win_loss}, mid={mid}"
        )
        self.navigate_to_tab(self.sessions_tab.session_tab)
        self.ui_utils.click_to_element(self.sessions_tab.create_manual_rating_btn)
        self.ui_utils.click_to_element(self.sessions_tab.seat_number)
        self.ui_utils.click_to_element(self.sessions_tab.get_seat_option(seat_num))
        self.ui_utils.fill_element(self.sessions_tab.player_id_textbox, player_id)
        self.ui_utils.press_enter(self.sessions_tab.player_id_textbox)
        self.ui_utils.click_to_element(self.sessions_tab.first_player_item)
        self.ui_utils.click_to_element(self.sessions_tab.start_time)
        self.ui_utils.click_to_element(self.sessions_tab.minus_hour_btn)
        self.ui_utils.click_to_element(self.sessions_tab.set_btn)
        self.ui_utils.click_to_element(self.sessions_tab.stop_time)
        self.ui_utils.click_to_element(self.sessions_tab.set_btn)
        self.ui_utils.fill_element(self.sessions_tab.cash_buyin_textbox, str(buyin))
        self.ui_utils.fill_element(self.sessions_tab.average_bet_textbox, str(average_bet))
        self.ui_utils.fill_element(self.sessions_tab.casino_win_loss_textbox, str(casino_win_loss))
        if mid:
            self.ui_utils.fill_element(self.sessions_tab.mid_textbox, str(mid))
        self.ui_utils.click_to_element(self.sessions_tab.submit_btn)
        self.logger_utils.log(
            f"Manual rating submitted (Sessions tab) for player_id={player_id}, seat_num={seat_num}"
        )
        time.sleep(5)

    def submit_manual_rating_players_tab(self, player_id, seat_num, buyin, average_bet, casino_win_loss, mid=None):
        """
        Submits a manual rating for a player on Players tab.
        Args:
            player_id: Player ID to enter
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(
            f"Submitting manual rating (Players tab) for player_id={player_id}, seat_num={seat_num}, buyin={buyin}, average_bet={average_bet}, casino_win_loss={casino_win_loss}, mid={mid}"
        )
        self.navigate_to_tab(self.player_tab.Players_TAB)
        self.ui_utils.click_to_element(self.player_tab.get_seat_A_locator())
        self.ui_utils.click_to_element(self.player_tab.select_seat(seat_num))
        self.ui_utils.fill_element(self.player_tab.player_id_textbox, player_id)
        self.ui_utils.press_enter(self.player_tab.player_id_textbox)
        self.ui_utils.click_to_element(self.player_tab.first_player_item)
        self.ui_utils.click_to_element(self.player_tab.start_time)
        self.ui_utils.click_to_element(self.player_tab.minus_hour_btn)
        self.ui_utils.click_to_element(self.player_tab.set_btn)
        self.ui_utils.click_to_element(self.player_tab.stop_time)
        self.ui_utils.click_to_element(self.player_tab.set_btn)
        self.ui_utils.fill_element(self.player_tab.cash_buyin_textbox, str(buyin))
        self.ui_utils.fill_element(self.player_tab.average_bet_textbox, str(average_bet))
        self.ui_utils.fill_element(self.player_tab.casino_win_loss_textbox, str(casino_win_loss))
        self.ui_utils.fill_element(self.player_tab.mid_textbox, str(mid))
        if mid:
            self.ui_utils.fill_element(self.sessions_tab.mid_textbox, str(mid))
        self.ui_utils.click_to_element(self.player_tab.submit_btn)
        self.logger_utils.log(
            f"Manual rating submitted (Players tab) for player_id={player_id}, seat_num={seat_num}"
        )
        time.sleep(5)
        
    def save_manual_rating_players_tab(self, player_id, seat_num, buyin, average_bet, casino_win_loss, mid=None):
        """
        Save a manual rating for a player on Players tab.
        Args:
            player_id: Player ID to enter
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Saving manual rating for player_id={player_id}, seat_num={seat_num} on Players tab.")
        self.navigate_to_tab(self.player_tab.Players_TAB)
        self.ui_utils.click_to_element(self.player_tab.get_seat_A_locator())
        self.ui_utils.click_to_element(self.player_tab.select_seat(seat_num))
        self.ui_utils.fill_element(self.player_tab.player_id_textbox, player_id)
        self.ui_utils.press_enter(self.player_tab.player_id_textbox)
        self.ui_utils.click_to_element(self.player_tab.first_player_item)
        self.ui_utils.click_to_element(self.player_tab.start_time)
        self.ui_utils.click_to_element(self.player_tab.minus_hour_btn)
        self.ui_utils.click_to_element(self.player_tab.set_btn)
        self.ui_utils.fill_element(self.player_tab.cash_buyin_textbox, str(buyin))
        self.ui_utils.fill_element(self.player_tab.average_bet_textbox, str(average_bet))
        self.ui_utils.fill_element(self.player_tab.casino_win_loss_textbox, str(casino_win_loss))
        if mid:
            self.ui_utils.fill_element(self.player_tab.mid_textbox, str(mid))
        self.ui_utils.click_to_element(self.player_tab.save_btn)
        time.sleep(5)
        self.logger_utils.log(f"Manual rating saved for player_id={player_id}, seat_num={seat_num} on Players tab.")
              
    def save_manual_rating_sessions_tab(self, player_id, seat_num, buyin, average_bet, casino_win_loss, mid=None):
        """
        Submits a manual rating for a player on Sessions tab.
        Args:
            player_id: Player ID to enter
            seat_num: Seat number
            buyin: Cash Buy In value
            average_bet: Average Bet value
            casino_win_loss: Casino Win/Loss value
            mid: Manual ID (if needed)
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(
            f"Saving manual rating (Sessions tab) for player_id={player_id}, seat_num={seat_num}, buyin={buyin}, average_bet={average_bet}, casino_win_loss={casino_win_loss}, mid={mid}"
        )
        self.navigate_to_tab(self.sessions_tab.session_tab)
        self.ui_utils.click_to_element(self.sessions_tab.create_manual_rating_btn)
        self.ui_utils.click_to_element(self.sessions_tab.seat_number)
        self.ui_utils.click_to_element(self.sessions_tab.get_seat_option(seat_num))
        self.ui_utils.fill_element(self.sessions_tab.player_id_textbox, player_id)
        self.ui_utils.press_enter(self.sessions_tab.player_id_textbox)
        self.ui_utils.click_to_element(self.sessions_tab.first_player_item)
        self.ui_utils.click_to_element(self.sessions_tab.start_time)
        self.ui_utils.click_to_element(self.sessions_tab.minus_hour_btn)
        self.ui_utils.click_to_element(self.sessions_tab.set_btn)
        self.ui_utils.fill_element(self.sessions_tab.cash_buyin_textbox, str(buyin))
        self.ui_utils.fill_element(self.sessions_tab.average_bet_textbox, str(average_bet))
        self.ui_utils.fill_element(self.sessions_tab.casino_win_loss_textbox, str(casino_win_loss))
        if mid:
            self.ui_utils.fill_element(self.sessions_tab.mid_textbox, str(mid))
        self.ui_utils.click_to_element(self.sessions_tab.save_btn)
        time.sleep(5)
        self.logger_utils.log(
            f"Manual rating saved (Sessions tab) for player_id={player_id}, seat_num={seat_num}"
        )
           
    def chipOwnership_check(self, chip_details_data, player_ids):
        """
        Checks if all Owner values in the chip details data contain only the given player IDs.

        Args:
            chip_details_data (list): List of dicts as extracted from the chip details table.
            player_ids (list): List of player IDs to check for (e.g., ["6001", "6002"]).

        Returns:
            bool: True if all Owner values contain only the player IDs, False otherwise.
        """
        if not chip_details_data or not player_ids:
            return False
        owners = chip_details_data[0].get("Owner", [])
        # Extract just the player ID part from each Owner string (e.g., "Jain, Parul (6001)" -> "6001")
        def extract_id(owner_str):
            if "(" in owner_str and ")" in owner_str:
                return owner_str.split("(")[-1].split(")")[0].strip()
            return owner_str.strip()
        owner_ids = [extract_id(owner) for owner in owners]
        return all(owner_id in player_ids for owner_id in owner_ids)

    def is_owner_only_anonymous(self, chip_details_data):
        """
        Returns True if all Owner values contain only the word 'Anonymous'
        (with any numbers/special characters allowed after it), and no other words.

        Args:
            chip_details_data (list): List of dicts as extracted from the chip details table.

        Returns:
            bool: True if all Owner values contain only 'Anonymous' (with any numbers/special chars), False otherwise.
        """
        if not chip_details_data:
            return False
        owners = chip_details_data[0].get("Owner", [])
        pattern = r"^Anonymous[\s\S]*$"  # Starts with 'Anonymous', anything after is allowed
        return all(re.match(pattern, owner) for owner in owners)