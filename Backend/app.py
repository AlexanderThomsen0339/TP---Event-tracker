from flask import Flask
from flask_restx import Api, Resource

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTX API with Swagger UI available at /swagger
api = Api(app, doc='/doc')

# Define a simple /events route
@api.route('/events')
class EventsResource(Resource):
    def get(self):
        # Return a sample list of events in JSON format
        return [{"id": 1, "name": "Concert"}, {"id": 2, "name": "Festival"}]

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
    api.init_app(app)
