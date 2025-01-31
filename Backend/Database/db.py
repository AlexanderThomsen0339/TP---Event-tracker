import pyodbc
import os
from dotenv import load_dotenv

class database:
    def create_connection():
        try:
            conn_str = os.getenv('DB_CONNECTION_STRING')

            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor
            
            return cursor
        except Exception as e:
            print(f"Failed to connect to database!{e}")
            return None

    def close_connection(cnxn, cursor):
        try:
            if cursor:
                cursor.close()
            if cnxn:
                cnxn.close()
        except Exception as e:
            print(f"Fejl ved lukning af forbindelse: {e}")
