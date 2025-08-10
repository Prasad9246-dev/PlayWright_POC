from utils.TableActions import TableActions

class Payout:
    def __init__(self, page):
        self.page = page
        self.table_actions = TableActions(page)

    def process_payouts(self, table_ip, payout_data, chips_df):
        """
        For each payout entry, get chips for denom, move them to Dealer, then to the specified antenna.
        Args:
            table_ip: Table IP address as string.
            payout_data: List of dicts [{'antenna': ..., 'denom': ...}, ...] from get_payout_data.
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