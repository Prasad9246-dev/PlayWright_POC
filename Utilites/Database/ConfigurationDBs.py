import psycopg2

class ConfigurationAPI_DB:
    def __init__(self):
        pass

    def get_connection(self, tableIP):
        conn_str = (
            f"dbname=wdts_db "
            f"user=wdts_admin "
            f"password=35Password! "
            f"host={tableIP} "
            f"port=5432 "
            f"sslmode=disable"
        )
        try:
            conn = psycopg2.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            return None

    def get_game_template_id(self, tableIP, template_name):
        query = "SELECT template_id FROM t_template_configuration WHERE name = %s and template_type = 'GAME' limit 1;"
        conn = self.get_connection(tableIP)
        if conn is None:
            print("Could not establish database connection.")
            return None
        try:
            cur = conn.cursor()
            cur.execute(query, (template_name,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result:
                return result[0]
            else:
                print("No template found.")
                return None
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def run_query(self, tableIP, query):
        conn = self.get_connection(tableIP)
        if conn is None:
            print("Could not establish database connection.")
            return None
        try:
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Database error: {e}")
            return None

if __name__ == "__main__":
    pass