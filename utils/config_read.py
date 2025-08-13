from utils.excel_reader import read_excel_config

class ConfigUtils:
    def __init__(self):
        self.config = read_excel_config("data/config_data.xlsx")

    def get_config(self):
        return self.config

    def get_tableIP(self):
        table_ip = self.config.get("tableip")
        print(table_ip)
        return table_ip

    def get_username(self):
        return self.config.get("username")

    def get_password(self):
        return self.config.get("password")

    def get_env(self):
        return self.config.get("env")

    def get_ppApplication_Url(self):
        url_template = self.config.get("ppapplicationurl")
        env = self.config.get("env")
        print(f"url_template: {url_template}, env: {env}")
        if url_template and env:
            return url_template.replace("env", env)
        print(url_template)
        return url_template

    def get_url(self):
        url_template = self.config.get("url")
        table_ip = self.config.get("tableip")
        if url_template and table_ip:
            return url_template.replace("tableIP", table_ip)
        print(url_template)
        return url_template