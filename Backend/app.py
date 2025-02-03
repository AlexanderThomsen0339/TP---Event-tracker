from flask import Flask
from flasgger import Swagger
from Routes.event_routes import event_bp  # Importér din Blueprint-route

app = Flask(__name__)
Swagger(app)  # Initialiserer Swagger

# Registrér Blueprint
app.register_blueprint(event_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
