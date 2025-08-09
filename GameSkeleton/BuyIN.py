from utils.TableActions import TableActions
class BuyIN:
    def __init__(self,page):
        self.page = page
        self.table_actions = TableActions(page)

    def process_buyins(self, table_ip, buyin_data, chips_df):
        """
        Processes all buy-ins and returns a data table:
        [
            {"player": "P1", "denom": ..., "chips_ID": [...]},
            {"player": "P2", "denom": ..., "chips_ID": [...]},
            ...
        ]
        """
        result_table = []
        for player_label, pdata in buyin_data.items():
            chips_ID = self.table_actions.buy_in_type(
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
