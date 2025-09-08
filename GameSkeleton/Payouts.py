from Utilites.TableUtils.TableActions import TableActions

class Payout:
    def __init__(self, page, feature_name):
        self.page = page
        self.table_actions = TableActions(page, feature_name)

    def process_payouts(self, table_ip, payout_data, chips_df):
        """
        For each payout entry, get chips for denom, move them to Dealer, then to the specified antenna.
        Args:
            table_ip: Table IP address as string.
            payout_data: List of dicts [{'antenna': ..., 'denom': ...}, ...] from get_payout_data.
        
        Author:
            Prasad Kamble
        """
        for entry in payout_data:
            antenna = entry["antenna"]
            denom = entry["denom"]
            chip_ids = self.table_actions.get_chip_ids_for_denom(chips_df, denom)
            if chip_ids:
                chip_ids_str = ",".join(chip_ids)
                print(f"Moving chips to DEALER: Chips={chip_ids_str}")
                self.table_actions.move_chips_between_antennas(table_ip, "TT", "DEALER", chip_ids_str)
                self.page.wait_for_timeout(1000)
                print(f"Moving chips from DEALER to Antenna {antenna}: Chips={chip_ids_str}")
                self.table_actions.move_chips_between_antennas(table_ip, "DEALER", antenna, chip_ids_str)
                self.page.wait_for_timeout(1000)
            else:
                print(f"No chips available for payout: Antenna={antenna}, Denom={denom}")
                


    def payout_chips_to_antenna(self, chips_str, table_ip, target_antenna):
        """
        Moves chips from chips_data to the dealer antenna first, then to the target antenna.

        Args:
            chips_data (str): Comma-separated chip IDs as a string.
            table_ip (str): Table IP address.
            target_antenna (str): Antenna name where chips should be finally placed.

        Example chips_data:
            'e00540011226b3cb,e00540011226b40c,e00540011226b40f'
        """
        dealer_antenna = "DEALER"
        print(f"Moving chips {chips_str} to dealer...")
        self.table_actions.move_chips_between_antennas(table_ip, "TT", dealer_antenna, chips_str)
        print(f"Moving chips {chips_str} to {target_antenna}...")
        self.table_actions.move_chips_between_antennas(table_ip, dealer_antenna, target_antenna, chips_str)