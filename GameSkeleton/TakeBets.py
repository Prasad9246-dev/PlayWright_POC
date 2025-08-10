from utils.TableActions import TableActions
class TakeBets:
    def __init__(self, page):
        self.page = page
        self.table_actions = TableActions(page)

    def take(self, table_ip, wager_result, takebets_list):
        """
        Removes chips from antennas listed in takebets_list using wager_result data.
        Args:
            table_ip: Table IP address as string.
            wager_result: List of dicts from wager function.
            takebets_list: List of antenna names from get_takeBets_data.
        """
        for antenna in takebets_list:
            # Find all chips on this antenna in wager_result
            chips_to_remove = []
            for entry in wager_result:
                if entry["antenna"] == antenna and entry["chips_ID"]:
                    chips_to_remove.extend(entry["chips_ID"])
            if chips_to_remove:
                chip_ids_str = ",".join(chips_to_remove)
                print(f"Removing chips from antenna {antenna}: {chip_ids_str}")
                # Call chip move API to remove chips (example: move to DEALER)
                self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "false")
            else:
                print(f"No chips found on antenna {antenna} to remove.")