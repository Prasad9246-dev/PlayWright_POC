import psycopg2
from Utilites.Logs.LoggerUtils import LoggerUtils

class ConfigurationAPI_DB:
    def __init__(self,feature_name):
        self.feature_name = feature_name
        self.logger_utils = LoggerUtils(self.feature_name)

    def get_connection(self, tableIP):
        conn_str = (
            f"dbname=wdts_db "
            f"user=wdts_admin "
            f"password=35Password! "
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

    def get_game_template_id(self, tableIP, template_name):
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