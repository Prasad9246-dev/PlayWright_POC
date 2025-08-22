from utils.TableActions import TableActions
from utils.UIUtils import UIUtils
from pages.ViewTableTab import ViewTableTab
class BuyIN:
    def __init__(self,page):
        self.page = page
        self.table_actions = TableActions(page)
        self.ui_utils = UIUtils(page)
        self.view_table_tab = ViewTableTab(page)

    def buy_in_type(self, table_ip, player_id: str, seat_number: int, denom: str, buyin_type: str, chips_df):
        """
        Automates the Buy-In process for a given player, seat, and denom.
        Finds the chip IDs for the given denom from chips_df using get_chip_ids_for_denom or get_n_chips_for_denom.
        Returns the chip IDs used for the buy-in.
        :param table_ip: Table IP address
        :param player_id: The player ID as string (e.g., "6001")
        :param seat_number: The seat number as integer (e.g., 1)
        :param denom: The denomination value as string (e.g., "100" or "100-5")
        :param buyin_type: "rated", "known", or "anonymous"
        :param chips_df: DataFrame containing chip IDs and Denoms
        :return: List of chip IDs used for buy-in
        
        Author:
            Prasad Kamble
        """
        try:
            # Determine which function to use based on denom format
            if '-' in denom:
                chip_ids = self.table_actions.get_n_chips_for_denom(chips_df, denom)
            else:
                chip_ids = self.table_actions.get_chip_ids_for_denom(chips_df, denom)

            if not chip_ids:
                print(f"No chips found for denom {denom}")
                return []

            chip_ids_str = ",".join(chip_ids)

            self.table_actions.navigate_to_tab(self.view_table_tab.view_table_tab(), wait_time=2000)
            # Step 1: Move chips from TT to DEALER
            self.table_actions.move_chips_between_antennas(table_ip, "TT", "DEALER", chip_ids_str)
            self.page.wait_for_timeout(1000)
            self.ui_utils.is_quick_buy_in_present()
            self.ui_utils.is_buy_in_button_present()
            # Step 2: Buy-In UI process
            if buyin_type.lower() == "rated":
                print(seat_number)
                self.view_table_tab.seat_section(seat_number)
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().fill(player_id)
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().press('Enter')
                self.page.wait_for_timeout(1000)
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Rated Buy-In process completed for seat {seat_number} and player {player_id}.")
            elif buyin_type.lower() == "known":
                self.view_table_tab.player_search_box().fill(player_id)
                self.page.wait_for_timeout(1000)
                self.view_table_tab.player_search_box().press('Enter')
                self.page.wait_for_timeout(1000)
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Known Buy-In process completed for player {player_id}.")
            elif buyin_type.lower() == "anon":
                self.view_table_tab.buy_in_confirm_button().click()
                self.page.wait_for_timeout(1000)
                print(f"Anon Buy-In process completed for player {player_id}.")
            else:
                print(f"Unknown buyin_type '{buyin_type}' specified.")
                return []

            # Step 3: Move chips from DEALER to the seat's antenna
            self.table_actions.chip_move_antenna(table_ip, "DEALER", chip_ids_str, "false")
            self.page.wait_for_timeout(1000)
            return chip_ids
        except Exception as e:
            print(f"Error during Buy-In: {e}")
            return []

    def process_buyins(self, table_ip, buyin_data, chips_df):
        """
        Processes all buy-ins and returns a data table:
        [
            {"player": "P1", "denom": ..., "chips_ID": [...]},
            {"player": "P2", "denom": ..., "chips_ID": [...]},
            ...
        ]
        
        Author:
            Prasad Kamble
        """
        result_table = []
        for player_label, pdata in buyin_data.items():
            chips_ID = self.buy_in_type(
                table_ip=table_ip,
                player_id=pdata["player_id"],
                seat_number=pdata["seat_number"],
                denom=pdata["denom"],
                buyin_type=pdata["buyin_type"],
                chips_df=chips_df
            )
            result_table.append({
                "player": player_label,
                "denom": pdata["denom"],
                "chips_ID": chips_ID
            })
        return result_table
