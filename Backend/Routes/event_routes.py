from flask import Blueprint, jsonify
from flasgger import swag_from

event_bp = Blueprint('event', __name__)

@event_bp.route('/hello', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A simple hello world response',
            'examples': {
                'application/json': {"message": "Hello, World!"}
            }
        }
    }
})
def hello_world():
    return jsonify({"message": "Hello, World!"})
