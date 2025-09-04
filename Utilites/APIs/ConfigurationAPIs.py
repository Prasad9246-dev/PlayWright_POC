import requests
import urllib3
from Utilites.Logs.LoggerUtils import LoggerUtils
from Utilites.ExcelRead.ExcelReader import get_file_path
from Utilites.Database.ConfigurationDBs import ConfigurationAPI_DB
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConfigurationAPIs:
    def __init__(self, feature_name):
        self.feature_name = feature_name
        self.configuration_db = ConfigurationAPI_DB(self.feature_name)
        self.password = get_file_path("password")
        self.logger_utils = LoggerUtils(self.feature_name)

    def get_access_token(self, base_url):
        """
        Requests and returns an access token from the configuration API.

        Args:
            base_url (str): The base URL of the configuration API (e.g., gateway URL).

        Returns:
            str or None: The access token string if successful, otherwise None.

        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Requesting access token from base_url: {base_url}")
        base_url = base_url.rstrip('/').replace('/login', '')
        token_url = f"{base_url}/api/auth/v1/oauth/token/login?client_id={'conf'}"
        payload = {
            "clientId": "conf",
            "authenticated": False,
            "username": "ppmaster",
            "pin": self.password
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
        """
        Updates the template properties for a given table and template type.

        Args:
            properties (list of tuple): List of (property_code, property_value) pairs to update.
                Example: [("com.wdts.manualrating.approval.criteria.averagebet", "100")]
            base_url (str): The base URL of the configuration API (e.g., gateway URL).
            table_ip (str): The IP address of the table whose template is being updated.
            template_type (str): The type of template to update (e.g., "SYSTEM", "TABLE", etc.).

        Returns:
            Response: The HTTP response object from the PUT request.

        Author:
            Prasad Kamble
        """
        base_url = base_url.rstrip('/').replace('/login', '')
        self.logger_utils.log(f"Requesting access token for template update: base_url={base_url}")
        access_token = self.get_access_token(base_url)
        self.logger_utils.log(f"Fetching template ID for table_ip={table_ip}, template_type={template_type}")
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
        self.logger_utils.log(f"Sending PUT request to {url} with payload: {payload}")
        response = requests.put(url, json=payload, headers=headers, verify=False)
        self.logger_utils.log(f"Update Template Response: {response.status_code} - {response.text}")
        print(f"Update Template Response: {response.status_code}")
        return response

    def get_current_template(self, tableIP, base_url, template_type):
        """
        Fetches the current template name for the given table IP and template type.

        Args:
            tableIP (str): The IP address of the table.
            base_url (str): The base URL of the configuration API (e.g., gateway URL).
            template_type (str): The type of template to fetch (e.g., "SYSTEM", "TABLE", etc.).

        Returns:
            str or None: The name of the current template, or None if not found.

        Author:
            Prasad Kamble
        """
        base_url = base_url.rstrip('/').replace('/login', '')
        self.logger_utils.log(f"Requesting access token for fetching current template: base_url={base_url}")
        access_token = self.get_access_token(base_url)
        self.logger_utils.log(f"Fetching template ID for tableIP={tableIP}, template_type={template_type}")
        template_id = self.get_current_template_id(base_url, tableIP, template_type)
        if not template_id:
            print("No templateId found for given tableIP and template_type.")
            return None
        url = f"{base_url}/api/configuration/v1/template?templateId={template_id}&templateType={template_type}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.logger_utils.log(f"Requesting template details from: {url}")
        response = requests.get(url, headers=headers, verify=False)
        try:
            data = response.json()
            template_name = data.get("name")
            self.logger_utils.log(f"Received template name: {template_name}")
            return template_name
        except Exception as e:
            msg = f"Error extracting template details: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None

    def update_system_tab(self, base_url, property_code, property_value):
        """
        Updates a single property in the SYSTEM template.

        Args:
            base_url (str): The base URL of the configuration API (e.g., gateway URL).
            property_code (str): The property code to update (e.g., "com.wdts.manualrating.approval.criteria.averagebet").
            property_value (str): The value to set for the property.

        Returns:
            Response: The HTTP response object from the PUT request.

        Author:
            Prasad Kamble
        """
        base_url = base_url.rstrip('/').replace('/login', '')
        self.logger_utils.log(f"Requesting access token for SYSTEM tab update: base_url={base_url}")
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
        self.logger_utils.log(f"Sending PUT request to {url} with payload: {payload}")
        response = requests.put(url, json=payload, headers=headers, verify=False)
        self.logger_utils.log(f"Update SYSTEM Tab Response: {response.status_code} - {response.text}")
        print(f"Update SYSTEM Tab Response: {response.status_code}")
        return response
    
    def update_game_template(self, base_url, table_ip, properties):
        """
        Updates the GAME template properties for a given table.

        Args:
            base_url (str): The base URL of the configuration API (e.g., gateway URL).
            table_ip (str): The IP address of the table whose template is being updated.
            properties (list of tuple): List of (property_code, property_value) pairs to update.
                Example: [
                    ("com.wdts.manualrating.approval.criteria.averagebet", 100000),
                    ("com.wdts.manualrating.approval.criteria.buyin", 100000),
                    ("com.wdts.manualrating.approval.criteria.casinowl", 100000)
                ]

        Returns:
            Response: The HTTP response object from the PUT request.

        Author:
            Prasad Kamble
        """
        base_url = base_url.rstrip('/').replace('/login', '')
        self.logger_utils.log(f"Requesting access token for GAME template update: base_url={base_url}")
        access_token = self.get_access_token(base_url)
        template_type = "GAME"
        table_info = self.get_table_info(table_ip)
        game_template_name = table_info.get("gameTemplate")
        self.logger_utils.log(f"Fetching template ID for table_ip={table_ip}, template_type={template_type}")
        template_id = self.configuration_db.get_game_template_id(table_ip, game_template_name)
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
        self.logger_utils.log(f"Sending PUT request to {url} with payload: {payload}")
        response = requests.put(url, json=payload, headers=headers, verify=False)
        self.logger_utils.log(f"Update GAME Template Response: {response.status_code} - {response.text}")
        print(f"Update GAME Template Response: {response.status_code}")
        return response