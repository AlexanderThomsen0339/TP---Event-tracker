from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from Routes.user_routes import ns_events as users_ns
from Routes.event_routes import ns_events as events_ns

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes globally with credentials support
CORS(app, supports_credentials=True)

# Attach RESTX API to the main app (ensures Swagger works)
api = Api(app, doc='/doc')

# Register the namespaces
api.add_namespace(events_ns, path='/api/events')
api.add_namespace(users_ns, path='/api/users')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
