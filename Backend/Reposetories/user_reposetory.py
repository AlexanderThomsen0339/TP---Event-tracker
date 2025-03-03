from Database.db import Database
import pyodbc

def create_user(username, password):
    db = Database()
    db.create_connection()

    conn = db.conn  
    cursor = conn.cursor()

    try:
        # Kald den stored procedure
        cursor.execute("EXEC CreateUser @Username = ?, @Password = ?", username, password)
        conn.commit()
        print("Bruger oprettet succesfuldt.")
        
    except pyodbc.Error as e:
        print(f"Fejl ved oprettelse af bruger: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_by_name(username):
    db = Database()
    db.create_connection()

    conn = db.conn
    cursor = conn.cursor()

    try:
        cursor.execute("EXEC GetUser @Username = ?;", username)

        user = cursor.fetchone()  # Hent én række

        if user:  # Hvis brugeren findes
            return {
                "username": user[0],  # Første kolonne er Username
                "password": user[1]    # Anden kolonne er Password (hashed)
            }
        else:
            return None
    except pyodbc.Error as e:
        print(f"Fejl ved exekvering af procedure: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
