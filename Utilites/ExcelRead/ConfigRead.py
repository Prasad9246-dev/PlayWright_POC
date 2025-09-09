from logging import config
import os
from Utilites.ExcelRead.ExcelReader import read_excel_config ,get_file_path

class ConfigUtils:
    
    def __init__(self):
        self.username = os.getlogin()
        self.feature_name = None
        self.config_path = None
        self.config = None

    def set_feature_name(self, feature_name):
        self.feature_name = feature_name
        self.config_path = os.path.join(get_file_path("configPath"),self.feature_name + ".xlsx")
        self.config = read_excel_config(self.config_path)

    def get_config(self):
        """Returns the entire configuration dictionary.
        Author:
            Prasad Kamble
        """
        return self.config

    def get_tableIP(self):
        """
        Returns the Table IP address, prioritizing runtime environment variable if set.
        Author:
        Prasad Kamble
        """
        if getattr(self, "table_ip", None):
            return self.table_ip
        runtime_table_ip = os.getenv("RUNTIME_TABLE_IP")
        self.table_ip = runtime_table_ip if runtime_table_ip is not None else self.config.get("tableip")
        return self.table_ip

    def get_managementIP(self):
        """
        Returns the Management IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "management_ip", None):
            return self.management_ip
        runtime_management_ip = os.getenv("RUNTIME_MANAGEMENT_IP")
        self.management_ip = runtime_management_ip if runtime_management_ip is not None else self.config.get("managementip")
        return self.management_ip

    def get_transactionIP(self):
        """
        Returns the Transaction IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "transaction_ip", None):
            return self.transaction_ip
        runtime_transaction_ip = os.getenv("RUNTIME_TRANSACTION_IP")
        self.transaction_ip = runtime_transaction_ip if runtime_transaction_ip is not None else self.config.get("transactionip")
        return self.transaction_ip

    def get_integrationIP(self):
        """
        Returns the Integration IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "integration_ip", None):
            return self.integration_ip
        runtime_integration_ip = os.getenv("RUNTIME_INTEGRATION_IP")
        self.integration_ip = runtime_integration_ip if runtime_integration_ip is not None else self.config.get("integrationip")
        return self.integration_ip

    def get_cmsIP(self):
        """
        Returns the CMS IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "cms_ip", None):
            return self.cms_ip
        runtime_cms_ip = os.getenv("RUNTIME_CMS_IP")
        self.cms_ip = runtime_cms_ip if runtime_cms_ip is not None else self.config.get("cmsip")
        return self.cms_ip

    def get_cageIP(self):
        """
        Returns the Cage IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "cage_ip", None):
            return self.cage_ip
        runtime_cage_ip = os.getenv("RUNTIME_CAGE_IP")
        self.cage_ip = runtime_cage_ip if runtime_cage_ip is not None else self.config.get("cageip")
        return self.cage_ip

    def get_externalKafkaIP(self):
        """
        Returns the External Kafka IP, prioritizing runtime environment variable if set.
        Author:
            Prasad Kamble
        """
        if getattr(self, "external_kafka_ip", None):
            return self.external_kafka_ip
        runtime_kafka_ip = os.getenv("RUNTIME_EXTERNAL_KAFKA_IP")
        self.external_kafka_ip = runtime_kafka_ip if runtime_kafka_ip is not None else self.config.get("externalkafkaip")
        return self.external_kafka_ip

    def get_tableType(self):
        """
        Returns the Table Type from config.
        Author:
            Prasad Kamble
        """
        return self.config.get("tabletype")

    def get_username(self):
        """
        Returns the username.
        Author:
            Prasad Kamble
        """
        return self.config.get("username")
    
    def get_build_version(self):
        """
        Returns the build version from the given config dictionary.

        Args:
            config (dict): Configuration dictionary containing 'build_version' key.

        Returns:
            str: The build version, or an empty string if not found.
        """
        return self.config.get("build_version")

    def get_password(self):
        """Returns the password.
        Author:
            Prasad Kamble
        """
        return self.config.get("password")

    def get_env(self):
        """Returns the environment.
        Author:
            Prasad Kamble
        """
        return self.config.get("env")

    def get_ppApplication_Url(self):
        """Returns the PP Application URL.
        Author:
            Prasad Kamble
        """
        url_template = get_file_path("ppapplicationurl")
        env = self.config.get("env")
        if url_template and env:
            return url_template.replace("env", env)
        print(url_template)
        return url_template

    def get_table_url(self):
        """Returns the URL.
        Author:
            Prasad Kamble
        """
        url_template = get_file_path("tableurl")
        table_ip = self.get_tableIP()
        if url_template and table_ip:
            return url_template.replace("tableIP", table_ip)
        print(url_template)
        return url_template
    
    def get_cageURL(self):
        """
        Returns the Cage URL from config.
        Author:
            Prasad Kamble
        """
        url_template = get_file_path("cageurl")
        cage_ip = self.get_cageIP()
        if url_template and cage_ip:
            return url_template.replace("CageIP", cage_ip)
        print(url_template)
        return url_template