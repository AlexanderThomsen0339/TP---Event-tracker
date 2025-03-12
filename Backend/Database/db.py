import pyodbc
import os
from dotenv import load_dotenv

# Indlæs miljøvariabler
load_dotenv()

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def create_connection(self):
        try:
            print(str(os.getenv("DRIVER")))
            print(str(os.getenv("DATABASE")))
            driver = os.getenv("DRIVER")
            database = os.getenv("DATABASE")
            conn_str = f'driver={driver};server=(LocalDb)\\MSSQLLocalDB;database={database};trusted_connection=yes;'
            self.conn = pyodbc.connect(conn_str)  
            self.cursor = self.conn.cursor() 
        except Exception as e:
            print(f"Fejl ved oprettelse af forbindelse: {e}")
            return None

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Fejl ved lukning af forbindelse: {e}")

    def execute_query(self, query, params=None):
        """Udfører en SQL-forespørgsel, med mulighed for at bruge parametre."""
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()  # Sikre, at ændringer bliver gemt
        except Exception as e:
            print(f"Fejl ved udførelse af forespørgsel: {e}")

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Fejl ved hentning af data: {e}")
            return []

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Fejl ved hentning af én række: {e}")
            return None
