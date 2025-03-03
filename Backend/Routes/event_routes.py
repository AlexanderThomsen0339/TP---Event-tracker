from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from Services.Ticketmaster_services import get_ticketmaster_events
from Services.event_services import get_events_from_radius
import Reposetories.event_reposetory
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a Namespace for better organization
ns_events = Namespace('events', description='Event-related operations')

location_model = ns_events.model('GetEventsWithinRadius', {
    'radius': fields.String(required=True, description='Radius in kilometers'),
    'latitude': fields.String(required=True, description='Latitude of the location'),
    'longitude': fields.String(required=True, description='Longitude of the location')
})

@ns_events.route('/get_ticketmaster_events_dk')
class TicketmasterEventsDK(Resource):
    def post(self):
        try:
            events = get_ticketmaster_events()  # Kald den nye funktion
            if not events:
                return {"error": "No events found in Denmark."}, 404

            Reposetories.event_reposetory.save_events(events)
            return jsonify({"message": f"{len(events)} events successfully retrieved and saved!"})

        except Exception as e:
            logging.error(f"Error while retrieving or saving events: {str(e)}")
            return {"error": f"Error: {str(e)}"}, 500

@ns_events.route('/get_users_within_radius', methods=['POST'])
class Handle_events(Resource):
    def options(self):
        return {"message": "CORS preflight successful"}, 200
    
    @ns_events.expect(location_model)
    def post(self):
        radius = request.json.get('radius')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')

        if not all([radius, latitude, longitude]):
            return {"error": "Missing required fields (radius, latitude, or longitude)"}, 400

        try:
            events = get_events_from_radius(radius, latitude, longitude)

            if not events:
                return {"message": "No events found within the specified radius"}, 404

            return jsonify({"events": events})

        except Exception as e:
            logging.error(f"Error while getting events within radius: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}, 500