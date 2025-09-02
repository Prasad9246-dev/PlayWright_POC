import requests
import urllib3
from Utilites.Logs.LoggerUtils import LoggerUtils
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConfigurationAPIs:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.logger_utils = LoggerUtils(self.feature_name)

    def get_access_token(self, base_url):
        self.logger_utils.log(f"Requesting access token from base_url: {base_url}")
        base_url = base_url.rstrip('/').replace('/login', '')
        token_url = f"{base_url}/api/auth/v1/oauth/token/login?client_id={'conf'}"
        payload = {
            "clientId": "conf",
            "authenticated": False,
            "username": "ppmaster",
            "pin": "35Ramrod!"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
        response = requests.post(token_url, json=payload, headers=headers, verify=False)
        try:
            access_token = response.json().get("access_token")
            self.logger_utils.log(f"Received access token: {access_token}")
            return access_token
        except Exception as e:
            msg = f"Error extracting access_token: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None

    def get_table_info(self, table_ip):
        """
        Fetches table information from the table API using the given table IP.
        Returns the response JSON or text if JSON parsing fails.
        Author:
            Prasad Kamble
        """
        url = f"https://{table_ip}:790/api/table/v1/tableInfo"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        self.logger_utils.log(f"Requesting table info from: {url}")
        response = requests.get(url, headers=headers, verify=False)
        try:
            data = response.json()
            self.logger_utils.log(f"Received table info: {data}")
            return data
        except Exception as e:
            msg = f"Error parsing table info response: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            self.logger_utils.log(f"Raw response: {response.text}")
            print(msg)
            return response.text

    def get_current_template_id(self, base_url, table_ip, template_type):
        """
        Fetches the current template ID for the given table IP and template type.
        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Getting current template ID for table_ip={table_ip}, template_type={template_type}")
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        table_info = self.get_table_info(table_ip)
        topology_id = table_info.get("topologyId")
        url = f"{base_url}/api/configuration/v1/topology/template?templateType={template_type}&topologyId={topology_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.logger_utils.log(f"Requesting template ID from: {url}")
        response = requests.get(url, headers=headers, verify=False)
        try:
            data = response.json()
            template_id = data.get("templateId")
            self.logger_utils.log(f"Received template ID: {template_id}")
            return template_id
        except Exception as e:
            msg = f"Error extracting templateId: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None

    def update_template(self, properties, base_url, table_ip, template_type):
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        template_id = self.get_current_template_id(base_url, table_ip, template_type)
        print(f"Updating template: {template_id}, properties: {properties}")
        updated_by = "Master, PP (0)"
        property_dict = {
            prop: {"defaultValue": val}
            for prop, val in properties
        }
        url = f"{base_url}/api/configuration/v1/template"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "templateId": template_id,
            "templateType": template_type,
            "templatePropertyByPropertyCode": property_dict,
            "updatedBy": updated_by
        }
        response = requests.put(url, json=payload, headers=headers, verify=False)
        print(f"Update Template Response: {response.status_code}")
        return response

    def get_current_template(self, tableIP, base_url, template_type):
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        template_id = self.get_current_template_id(base_url, tableIP, template_type)
        if not template_id:
            print("No templateId found for given tableIP and template_type.")
            return None
        url = f"{base_url}/api/configuration/v1/template?templateId={template_id}&templateType={template_type}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, verify=False)
        try:
            data = response.json()
            return data.get("name")
        except Exception as e:
            print(f"Error extracting template details: {e}")
            return None

    def update_system_tab(self, base_url, property_code, property_value):
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        template_type = "SYSTEM"
        url = f"{base_url}/api/configuration/v1/template"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "templateId": "1",
            "templateType": template_type,
            "templatePropertyByPropertyCode": {
                property_code: {
                    "defaultValue": property_value
                }
            },
            "updatedBy": "Master, PP (0)"
        }
        response = requests.put(url, json=payload, headers=headers, verify=False)
        print(f"Update SYSTEM Tab Response: {response.status_code}")
        return response