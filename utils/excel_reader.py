import openpyxl
import pandas as pd

def read_excel_config(path):
    """
    Reads a key-value config Excel file (first column: key, second column: value).
    Returns a dictionary with lowercase, stripped keys.
    Author:
            Prasad Kamble
    """
    config = {}
    try:
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            key, value = row
            if key is not None:
                key_clean = key.strip().lower()
                value_clean = str(value).strip() if value is not None else ""
                config[key_clean] = value_clean
    except Exception as e:
        print(f"Error reading Excel file: {e}")
    return config

def read_chip_ids_df(path):
    """
    Reads the 'ChipIds' sheet and returns a DataFrame with 'chipsID' and 'Denom'.
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(path, sheet_name="ChipIds")
    return df[["All-chips", "Denom"]].rename(columns={"All-chips": "chipsID"})

def get_buyin_data(excel_path, test_case_id):
    """
    Reads all buyIn columns for the given test_case_id and returns a dict:
    { 'P1': {...}, 'P2': {...}, ... }
    Handles missing seat/player_id for known/anon types.
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(excel_path)
    if test_case_id not in df['testCase_ID'].values:
        print(f"Test case ID '{test_case_id}' not present in test data")
        return {}
    row = df[df['testCase_ID'] == test_case_id].iloc[0]
    buyin_dict = {}
    idx = 1
    for col in df.columns:
        if col.lower().startswith("buyin") and pd.notna(row[col]):
            parts = [p.strip() for p in str(row[col]).split(';')]
            denom = parts[0] if len(parts) > 0 else None
            type_id = parts[1] if len(parts) > 1 else None
            seat = parts[2] if len(parts) > 2 else None

            buyin_type = None
            player_id = None
            seat_number = None

            if type_id:
                if '-' in type_id:
                    buyin_type, player_id = type_id.split('-', 1)
                else:
                    buyin_type = type_id
            if seat:
                try:
                    seat_number = int(seat)
                except Exception:
                    seat_number = None

            buyin_data = {
                "denom": denom,
                "buyin_type": buyin_type.lower() if buyin_type else None,
                "player_id": player_id,
                "seat_number": seat_number
            }
            # Optionally add extra fields if present
            if len(parts) > 3:
                buyin_data["extra"] = parts[3:]
            buyin_dict[f"P{idx}"] = buyin_data
            idx += 1
    return buyin_dict
    
def get_wager_data(excel_path, test_case_id):
    """
    Reads all wager columns for the given test_case_id and returns a dict:
    { 'W1': {...}, 'W2': {...}, ... }
    Handles any number of wager columns, including tagged bets.
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(excel_path)
    # row = df[df['testCase_ID'] == test_case_id].iloc[0]
    if test_case_id not in df['testCase_ID'].values:
        print(f"Test case ID '{test_case_id}' not present in test data")
        return {}
    row = df[df['testCase_ID'] == test_case_id].iloc[0]
    wager_dict = {}
    idx = 1
    for col in df.columns:
        # Accept columns that start with "wager" or contain "wager" or "Player(wager"
        if ("wager" in col.lower() or "player(wager" in col.lower()) and pd.notna(row[col]):
            parts = [p.strip() for p in str(row[col]).split(';')]
            player = parts[0] if len(parts) > 0 else None
            denom = parts[1] if len(parts) > 1 else None
            antenna = parts[2] if len(parts) > 2 else None
            wager_data = {
                "player": player,
                "denom": denom,
                "antenna": antenna
            }
            # Support tagged bets (4th part)
            if len(parts) > 3:
                wager_data["tagged_antenna"] = parts[3]
            wager_dict[f"W{idx}"] = wager_data
            idx += 1
    return wager_dict

def get_cards_data(excel_path, test_case_id):
    """
    Reads card columns (card1, card2, ...) for the given test_case_id and returns a list of card values.
    Example return: ['2s', '4d', '3s', '4d']
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(excel_path)
    # row = df[df['testCase_ID'] == test_case_id].iloc[0]
    if test_case_id not in df['testCase_ID'].values:
        print(f"Test case ID '{test_case_id}' not present in test data")
        return {}
    row = df[df['testCase_ID'] == test_case_id].iloc[0]
    cards = []
    for col in df.columns:
        if col.lower().startswith("card") and pd.notna(row[col]):
            cards.append(str(row[col]).strip())
    return cards

def get_takeBets_data(excel_path, test_case_id):
    """
    Reads the TakeBets column for the given test_case_id and returns a list of bets, split by ';'.
    Example return: ['B3', 'B5']
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(excel_path)
    # row = df[df['testCase_ID'] == test_case_id].iloc[0]
    if test_case_id not in df['testCase_ID'].values:
        print(f"Test case ID '{test_case_id}' not present in test data")
        return {}
    row = df[df['testCase_ID'] == test_case_id].iloc[0]
    takebets_raw = row.get("TakeBets", "")
    if pd.notna(takebets_raw):
        bets = [bet.strip() for bet in str(takebets_raw).split(';') if bet.strip()]
        return bets
    return []

def get_payout_data(excel_path, test_case_id):
    """
    Reads all payout columns (payAmt1;Antenna, payAmt2, ...) for the given test_case_id
    and returns a list of dicts: [{'antenna': ..., 'denom': ...}, ...]
    Handles any number of payout columns.
    Example return: [{'antenna': 'P1', 'denom': '100'}, {'antenna': 'P2', 'denom': '100'}, ...]
    Author:
            Prasad Kamble
    """
    df = pd.read_excel(excel_path)
    # row = df[df['testCase_ID'] == test_case_id].iloc[0]
    if test_case_id not in df['testCase_ID'].values:
        print(f"Test case ID '{test_case_id}' not present in test data")
        return {}
    row = df[df['testCase_ID'] == test_case_id].iloc[0]
    payout_list = []
    for col in df.columns:
        if col.lower().startswith("payamt"):
            val = row[col]
            if pd.notna(val):
                parts = [p.strip() for p in str(val).split(';')]
                antenna = parts[0] if len(parts) > 0 else None
                denom = parts[1] if len(parts) > 1 else None
                payout_list.append({
                    "antenna": antenna,
                    "denom": denom
                })
    return payout_list