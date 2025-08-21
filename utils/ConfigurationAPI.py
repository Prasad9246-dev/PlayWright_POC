import requests
 
class ConfigurationAPI:
    def __init__(self):
        pass
 
    def get_access_token(self, base_url):
        """
        Gets access token from the authentication API.
        - base_url: The base config URL (e.g., "https://wdts-gateway-cs01.wdts.local:792")
        Reads username, pin, and client_id from config.
        Returns: Response object from requests.post
        """
       
        # Remove '/login' from base_url if present
        base_url = base_url.rstrip('/').replace('/login', '')
 
        token_url = f"{base_url}/api/auth/v1/oauth/token/login?client_id={"conf"}"
        # print(f"Token URL: {token_url}")
 
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
            # print(f"Access Token: {access_token}")
            return access_token
        except Exception as e:
            print(f"Error extracting access_token: {e}")
            return None
 
    def get_table_info(self, table_ip):
        """
        Calls the tableInfo API using the provided table_ip and access_token.
        Returns: Response object from requests.get
        """
        url = f"https://{table_ip}:790/api/table/v1/tableInfo"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, verify=False)
        try:
            return response.json()
        except Exception:
            return response.text
 
    def get_current_template_id(self, base_url, table_ip, template_type):
        """
        Calls the topology template API and returns the templateId for the given table_ip.
        - base_url: The base URL (e.g., "https://wdts-gateway-cs01.wdts.local:792")
        - table_ip: The table IP address (e.g., "172.31.3.83")
        - access_token: Bearer token string
        - template_type: The templateType value (e.g., "TABLE")
        Returns: templateId value if present, else None
        """
        # Remove '/login' from base_url if present
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        table_info = self.get_table_info(table_ip)
        topology_id = table_info.get("topologyId")
        url = f"{base_url}/api/configuration/v1/topology/template?templateType={template_type}&topologyId={topology_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, verify=False)
        try:
            data = response.json()
            template_id = data.get("templateId")
            return template_id
        except Exception as e:
            print(f"Error extracting templateId: {e}")
            return None
 
    def update_template(self, properties, base_url, table_ip, template_type):
        """
        Updates multiple template properties using the configuration API.
        - properties: List of tuples [(property_code, value), ...]
        - base_url: The base URL for the API (e.g., "https://wdts-gateway-cs01.wdts.local:796")
        - table_ip: The table IP address (e.g., "172.31.3.83")
        - template_type: The templateType value (e.g., "TABLE")
        """
        base_url = base_url.rstrip('/').replace('/login', '')
        access_token = self.get_access_token(base_url)
        template_id = self.get_current_template_id(base_url, table_ip, template_type)
        print(f"Updating template: {template_id}, properties: {properties}")
        updated_by = "Master, PP (0)"
   
        # Build the property dictionary for the payload
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