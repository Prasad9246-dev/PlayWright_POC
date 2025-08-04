import openpyxl

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

if __name__ == "__main__":
    config = read_excel_config("data/config_data.xlsx")  # Update path if needed
    print(str(config))  # Optional: See output in terminal
