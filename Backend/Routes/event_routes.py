from flask import Blueprint, jsonify

# Define the event_routes Blueprint
event_bp = Blueprint('event_routes', __name__)

# Define the /events route
@event_bp.route('/events', methods=['GET'])
def get_events():
    # Return a sample list of events in JSON format
    return jsonify([{"id": 1, "name": "Concert"}, {"id": 2, "name": "Festival"}])
