import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConfigurationAPIs:
    def __init__(self):
        pass

    def get_access_token(self, base_url):
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
            return access_token
        except Exception as e:
            print(f"Error extracting access_token: {e}")
            return None

    def get_table_info(self, table_ip):
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

if __name__ == "__main__":
    pass