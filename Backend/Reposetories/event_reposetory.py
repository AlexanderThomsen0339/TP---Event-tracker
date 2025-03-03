from Database.db import Database
import pyodbc
from dotenv import load_dotenv
import logging

load_dotenv()

def save_events(events):
    db = Database()
    db.create_connection()

    conn = db.conn  
    cursor = conn.cursor()

    for event in events:
        event_name = "Ukendt event"  # Standardværdi for event_name
        try:
            # Extract event and location information
            location_name = event['_embedded']['venues'][0]['name']
            location_lat = event['_embedded']['venues'][0]['location']['latitude']
            location_lon = event['_embedded']['venues'][0]['location']['longitude']
            latlong = f"{location_lat},{location_lon}"

            event_name = event.get('name', 'Ukendt event')  # Hent event_name med en standardværdi
            event_start_time = event['dates']['start'].get('dateTime')
            api_id = event['id']

            if not event_start_time:
                logging.warning(f"⚠️ Missing 'dateTime' in event data '{event_name}'. Skipping this event.")
                continue  # Spring dette event over

            # Indsæt lokation i Locations-tabel
            cursor.execute("""
                INSERT INTO Locations (Location_Name, Location_LatLong)
                VALUES (?, ?);
            """, (location_name, latlong))
            cursor.execute("SELECT SCOPE_IDENTITY();")  # Hent den nye Location_ID
            location_id = cursor.fetchone()[0]  # Hent den nye Location_ID

            # Indsæt event i Events-tabel
            cursor.execute("""
                INSERT INTO Events (Event_Name, Event_Start_Time, Location_ID, API_ID)
                VALUES (?, ?, ?, ?);
            """, (event_name, event_start_time, location_id, api_id))
            cursor.execute("SELECT SCOPE_IDENTITY();")  # Hent den nye Event_ID
            event_id = cursor.fetchone()[0]  # Hent den nye Event_ID

            logging.info(f"✅ Event '{event_name}' saved in the database with Event_ID {event_id}.")
            conn.commit()  # Gem ændringerne

        except KeyError as e:
            logging.warning(f"⚠️ Missing key in event data '{event_name}': {str(e)}")
        except pyodbc.Error as e:
            logging.error(f"❌ Database error processing event '{event_name}': {str(e)}")
        except Exception as e:
            logging.error(f"❌ Unexpected error processing event '{event_name}': {str(e)}")

    cursor.close()
    db.close_connection()

def get_events_within_radius(radius,latitude, longitude):
    
    db = Database()
    db.create_connection()

    conn = db.conn  
    cursor = conn.cursor()

    sql = """
    EXEC GetEventsWithinRadius 
    @user_latitude = ?, 
    @user_longitude = ?, 
    @radius_km = ?;
    """
    cursor.execute(sql, (latitude, longitude, radius))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results  