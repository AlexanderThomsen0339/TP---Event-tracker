import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_ticketmaster_events():
    print("Henter alle events i Danmark (maks 49 sider)")
    base_url = "https://app.ticketmaster.com"
    initial_url = f"{base_url}/discovery/v2/events.json?apikey=W8FS6qW9RgDBoxZ3ADwYJeuBcb7DjJtd&countryCode=DK"
    all_events = []  # Samler alle events fra alle sider
    next_url = initial_url  # Start med den første URL
    page_count = 0  # Tæller for antal sider
    total_events = 0  # Tæller for samlet antal events
    max_pages = 49  # Maksimalt antal sider

    while next_url and page_count < max_pages:
        try:
            page_count += 1
            print(f"\nHenter side {page_count}: {next_url}")
            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()

            # Hent events fra den aktuelle side
            events = data.get('_embedded', {}).get('events', [])
            total_events += len(events)  # Opdater samlet antal events
            all_events.extend(events)  # Tilføj events til den samlede liste

            print(f"Events hentet på denne side: {len(events)}")
            print(f"Samlet antal events hentet: {total_events}")

            # Tjek om der er en næste side
            next_url = data.get('_links', {}).get('next', {}).get('href')
            if next_url:
                next_url = base_url + next_url  # Fuld URL til den næste side
                next_url = add_api_key(next_url)  # Tilføj API-nøgle til URL'en
            else:
                print("\nIngen flere sider tilbage.")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise Exception(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"API request failed: {req_err}")
            raise Exception(f"API request failed: {req_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")

    if not all_events:
        print("No events found.")
    elif page_count >= max_pages:
        print(f"\nMaksimalt antal sider ({max_pages}) nået. Stopper paginering.")

    return all_events

def add_api_key(url):
    """
    Tilføjer API-nøgle til en URL.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params["apikey"] = ["W8FS6qW9RgDBoxZ3ADwYJeuBcb7DjJtd"]  # Tilføj API-nøgle
    updated_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse(parsed_url._replace(query=updated_query))
    return updated_url