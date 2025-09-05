from Utilites.TableUtils.TableActions import TableActions
class TakeBets:
    def __init__(self, page, feature_name):
        self.page = page
        self.table_actions = TableActions(page, feature_name)

    def take(self, table_ip, wager_result, takebets_list):
        """
        Removes chips from antennas listed in takebets_list using wager_result data.
        Args:
            table_ip: Table IP address as string.
            wager_result: List of dicts from wager function.
            takebets_list: List of antenna names from get_takeBets_data.
        
        Author:
            Prasad Kamble
        """
        result_table = []
        for antenna in takebets_list:
            chips_to_remove = []
            for entry in wager_result:
                # Remove chips from main antenna
                if entry["antenna"] == antenna and entry["chips_ID"]:
                    chips_to_remove.extend(entry["chips_ID"])
                # Remove chips from tagged antenna if present
                if entry.get("tagged_antenna") == antenna and entry["chips_ID"]:
                    chips_to_remove.extend(entry["chips_ID"])
            if chips_to_remove:
                chip_ids_str = ",".join(chips_to_remove)
                print(f"Removing chips from antenna {antenna}: {chip_ids_str}")
                self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "false")
                result_table.append({"antenna": antenna, "chips_IDs": chips_to_remove})
            else:
                print(f"No chips found on antenna {antenna} to remove.")
                result_table.append({"antenna": antenna, "chips_IDs": []})
        return result_table