from Utilites.TableUtils.TableActions import TableActions
import time

class Wager:
    def __init__(self, page):
        self.table_actions = TableActions(page)

    def process_wagers(self, table_ip, buyin_result, wager_data):
        """
        For each wager, match player and denom with buyin_result,
        then place the correct chips on the specified antenna using chipMove API.
        Returns a list of processed wager entries.
        
        Author:
            Prasad Kamble
        """
        results = []
        for wager in wager_data.values():
            player = wager["player"]
            wager_amount = int(wager["denom"])  # e.g., 300
            antenna = wager["antenna"]
            tagged_antenna = wager.get("tagged_antenna")  # Optional for tagged bets

            # Find matching buy-in entry for the player
            match = next((entry for entry in buyin_result if entry["player"] == player), None)
            if not match:
                print(f"[SKIP] No matching buy-in for player {player}")
                continue

            chips_ID = match["chips_ID"]  # List of chip IDs
            buyin_denom = match["denom"]  # e.g., "100-5" or "100"
            # Get chip value and count from buyin_denom
            if '-' in str(buyin_denom):
                chip_value, chip_count = str(buyin_denom).split('-')
                chip_value = int(chip_value)
            else:
                chip_value = int(buyin_denom)

            # Select chips to match wager_amount
            chips_needed = wager_amount // chip_value
            selected_chips = chips_ID[:chips_needed]

            if len(selected_chips) < chips_needed or chips_needed == 0:
                print(f"[SKIP] Not enough chips to match wager {wager_amount} for player {player}")
                continue

            chip_ids_str = ",".join(selected_chips)
            if tagged_antenna:
                # Step 1: Move chips to main antenna with "true"
                print(f"[TAGGED] Placing chips for {player} on antenna {antenna}: {chip_ids_str} (true)")
                self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "true")
                time.sleep(1)
                # Step 2: Move chips to main antenna with "false"
                print(f"[TAGGED] Placing chips for {player} on antenna {antenna}: {chip_ids_str} (false)")
                self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "false")
                time.sleep(1)
                # Step 3: Move chips to tagged antenna with "true"
                print(f"[TAGGED] Moving chips for {player} to tagged antenna {tagged_antenna}: {chip_ids_str} (true)")
                self.table_actions.chip_move_antenna(table_ip, tagged_antenna, chip_ids_str, "true")
                time.sleep(1)
            else:
                print(f"[INFO] Placing chips for {player} (wager {wager_amount}) on antenna {antenna}: {chip_ids_str}")
                self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "true")
                time.sleep(1)

            results.append({
                "player": player,
                "denom": wager_amount,
                "antenna": antenna,
                "chips_ID": selected_chips,
                "tagged_antenna": tagged_antenna if tagged_antenna else None
            })
        return results