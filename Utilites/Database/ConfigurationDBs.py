import psycopg2
from Utilites.Logs.LoggerUtils import LoggerUtils
from Utilites.ExcelRead.ExcelReader import get_file_path

class ConfigurationAPI_DB:
    def __init__(self,feature_name):
        self.feature_name = feature_name
        self.logger_utils = LoggerUtils(self.feature_name)
        self.password = get_file_path("password")
        self.txn_password = get_file_path("txn_password")

    def get_connection(self, tableIP):
        """
        Establishes a connection to the WDTS configuration database using the provided table IP.

        Args:
            tableIP (str): The IP address of the table/database server.

        Returns:
            connection (psycopg2.extensions.connection or None): The database connection object if successful, otherwise None.

        Author:
            Prasad Kamble
        """
        conn_str = (
            f"dbname=wdts_db "
            f"user=wdts_admin "
            f"password={self.password} "
            f"host={tableIP} "
            f"port=5432 "
            f"sslmode=disable"
        )
        self.logger_utils.log(f"Attempting to connect to database at {tableIP}.")
        try:
            conn = psycopg2.connect(conn_str)
            self.logger_utils.log(f"Database connection established for {tableIP}.")
            return conn
        except Exception as e:
            msg = f"Database connection error for {tableIP}: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None
        
    def get_connection_txndb(self, txnIP):
        """
        Establishes a connection to the WDTS transaction database using the provided transaction IP.

        Args:
            txnIP (str): The IP address of the transaction database server.

        Returns:
            connection (psycopg2.extensions.connection or None): The transaction database connection object if successful, otherwise None.

        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Attempting to connect to transaction database at {txnIP}.")
        try:
            conn = psycopg2.connect(
                dbname="wdts_transactiondb",
                user="transaction_admin",
                password=self.txn_password,
                host=txnIP,
                port=5432,
                sslmode="disable"
            )
            self.logger_utils.log(f"Transaction DB connection established for {txnIP}.")
            return conn
        except Exception as e:
            msg = f"Transaction DB connection error for {txnIP}: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None

    def get_game_template_id(self, tableIP, template_name):
        """
        Fetches the GAME template_id for the given template name from the configuration database.

        Args:
            tableIP (str): The IP address of the table/database server.
            template_name (str): The name of the GAME template.

        Returns:
            int or None: The template_id if found, otherwise None.

        Author:
            Prasad Kamble
        """
        query = "SELECT template_id FROM t_template_configuration WHERE name = %s and template_type = 'GAME' limit 1;"
        self.logger_utils.log(f"Fetching GAME template_id for template_name='{template_name}' from tableIP={tableIP}.")
        conn = self.get_connection(tableIP)
        if conn is None:
            msg = "Could not establish database connection."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None
        try:
            cur = conn.cursor()
            cur.execute(query, (template_name,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                self.logger_utils.log(f"Found template_id: {result[0]} for template_name='{template_name}'.")
                return result[0]
            else:
                msg = f"No GAME template found for template_name='{template_name}'."
                self.logger_utils.log(f"[WARN] {msg}")
                print(msg)
                return None
        except Exception as e:
            msg = f"Database error while fetching GAME template_id: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None

    def run_query(self, tableIP, query):
        """
        Executes a SQL query on the WDTS configuration database for the given table IP.

        Args:
            tableIP (str): The IP address of the table/database server.
            query (str): The SQL query to execute.

        Returns:
            tuple or None: The first row of the query result as a tuple, or None if no result or error.

        Author:
            Prasad Kamble
        """
        self.logger_utils.log(f"Running query on {tableIP}: {query}")
        conn = self.get_connection(tableIP)
        if conn is None:
            msg = "Could not establish database connection."
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None
        try:
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            conn.close()
            self.logger_utils.log(f"Query result: {result}")
            return result
        except Exception as e:
            msg = f"Database error while running query: {e}"
            self.logger_utils.log(f"[ERROR] {msg}")
            print(msg)
            return None