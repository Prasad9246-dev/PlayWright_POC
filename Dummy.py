from playwright.sync_api import sync_playwright
import tkinter as tk
import requests
import json

def run():
    with sync_playwright() as p:
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.set_viewport_size({"width": screen_width, "height": screen_height})
        page.goto('https://wdts-gateway-cs01.wdts.local:792/login')
        page.get_by_role("textbox", name="Username").fill("ppmaster")
        page.get_by_role("textbox", name="Password").fill("35Ramrod!")
        page.get_by_role("textbox", name="Password").press("Enter")
        page.get_by_role("button", name="Configuration v.2.6.3.0").click()
        # browser.close()

def chip_move(table_ip, chip_id, antenna_name, acquired):
    """
    Sends a chip move request to the table API.

    Args:
        table_ip (str): Table IP address (e.g., '172.31.3.83').
        chip_id (str): Chip ID.
        antenna_name (str): Antenna name.
        acquired (bool or str): Acquired status (True/False or "true"/"false").

    Returns:
        Response object from requests.
    Author:
        Prasad Kamble
    """
    url = f"https://{table_ip}:790/api/table/v1/chipMove"
    payload = [{
        "chipId": chip_id,
        "antennaName": antenna_name,
        "acquired": str(acquired).lower() if isinstance(acquired, bool) else acquired
    }]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    return response

def update_template(token, template_data):
    """
    Updates a template using the configuration API.

    Args:
        token (str): Bearer token for authorization.
        template_data (dict): Template data payload.

    Returns:
        Response object from requests.
    Author:
        Prasad Kamble
    """
    url = "https://wdts-gateway-cs01.wdts.local:796/api/configuration/v1//template"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, data=json.dumps(template_data), verify=False)
    return response

# Example usage:
if __name__ == "__main__":
    resp = chip_move("172.31.3.83", "e00540011226b083", "P1", False)
    print(resp.status_code, resp.text)
    token = "eyJhbGciOiJFUzI1NiJ9.eyJsYXN0TmFtZSI6Ik1hc3RlciIsImlzcyI6IndkdGFibGVzeXN0ZW1zLmNvbSIsImVtcGxveWVlSWQiOiIwIiwibGFuZ3VhZ2UiOiJFTkdMSVNIIiwidXNlcklkIjoxLCJhdXRob3JpdGllcyI6W3sidG9wb2xvZ3lJZHMiOlsiU0VSVklDRVRPUCJdLCJwZXJtaXNzaW9ucyI6WyJTRVJWSUNFUEVSTSJdLCJhcHBsaWNhdGlvbkNvZGUiOiJDT05GSUdVUkFUSU9OIn1dLCJmaXJzdE5hbWUiOiJQUCIsIm5iZiI6MTc1NTczODcyNSwic2NvcGUiOltdLCJuYW1lIjoicHBtYXN0ZXIiLCJob3N0IjoiMTcyLjQxLjQwLjI1NCIsImV4cCI6MTc1NTg2MjMyNSwiaWF0IjoxNzU1ODU4NzI1LCJqdGkiOiJmNGEwNTM0My05MzEzLTQxY2QtYTcwOS00OWNjYzhkNDBhMjQiLCJzdXBlcnVzZXIiOnRydWUsImFwcGxpY2F0aW9ucyI6WyJDT05GSUdVUkFUSU9OIiwiVEFCTEVfTUkiLCJBTEVSVFMiLCJERUFMRVJfRElTUExBWSIsIkNBTSIsIkNBU0lOT19NR1IiLCJQTEFZRVJfREFTSCIsIlRSRUFTVVJZX01HUiIsIlJFUE9SVFMiLCJUQUJMRV9EQVNIIiwiTE9HSU4iLCJDQVNISUVSIl19.t-Kq_MzhYcIzjM3I0-BcnRUmG992gLx6qalRk5xc_k3kdWtC9e8pMY0HUIbVUvIC3iO8bmtGiRWOmvEgJnZv_Q"
    template_data = {
        "templateId": 1004,
        "templateType": "BUSINESS_RULES",
        "name": "BT-83",
        "topologyAccess": [51002],
        "templatePropertyByPropertyCode": {
            "com.wdts.bt.require.player.verification": {
                "defaultValue": "false"
            }
        },
        "updatedBy": "Master, PP (0)"
    }
    resp = update_template(token, template_data)
