import openpyxl
import pandas as pd

def read_excel_config(path):
    """
    Reads a key-value config Excel file (first column: key, second column: value).
    Returns a dictionary with lowercase, stripped keys.
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
    """
    df = pd.read_excel(path, sheet_name="ChipIds")
    return df[["All-chips", "Denom"]].rename(columns={"All-chips": "chipsID"})

print(read_chip_ids_df("data/AutomationChips.xlsx"))