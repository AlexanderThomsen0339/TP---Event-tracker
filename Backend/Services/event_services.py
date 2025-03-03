from Reposetories import event_reposetory

def get_events_from_radius(radius, latitude, longitude):
    # Hent events fra repository
    events = event_reposetory.get_events_within_radius(radius, latitude=latitude, longitude=longitude)

    # Hvis der ikke er nogen events, returner None
    if not events:
        return None
    
    # Konverter tuples til dictionaries
    event_list = []
    for event in events:
        event_dict = {
            "event_id": event[0],  # Event_ID
            "event_name": event[1],  # Event_Name
            "event_start_time": event[2],  # Event_Start_Time
            "location_name": event[3]  # Location_Name
        }
        event_list.append(event_dict)
    
    return event_list