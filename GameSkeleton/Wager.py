from utils.TableActions import TableActions
import time

class Wager:
    def __init__(self, page):
        self.table_actions = TableActions(page)

    def process_wagers(self, table_ip, buyin_result, wager_data):
        """
        For each wager, match player and denom with buyin_result,
        then place chips on the specified antenna using chipMove API.
        Returns a list of processed wager entries.
        """
        results = []
        for wager in wager_data.values():
            player = wager["player"]
            denom = wager["denom"]
            antenna = wager["antenna"]

            # Find matching buy-in entry
            match = next(
                (entry for entry in buyin_result if entry["player"] == player and str(entry["denom"]) == str(denom)),
                None
            )
            if not match:
                print(f"[SKIP] No matching buy-in for player {player} with denom {denom}")
                continue

            chips_ID = match["chips_ID"]
            if not chips_ID:
                print(f"[SKIP] No chips found for player {player} with denom {denom}")
                continue

            chip_ids_str = ",".join(chips_ID)
            print(f"[INFO] Placing chips for {player} (denom {denom}) on antenna {antenna}: {chip_ids_str}")
            # Place chips on antenna
            self.table_actions.chip_move_antenna(table_ip, antenna, chip_ids_str, "true")
            time.sleep(1)  # Wait for the chip move to complete
            results.append({
                "player": player,
                "denom": denom,
                "antenna": antenna,
                "chips_ID": chips_ID
            })
        return results