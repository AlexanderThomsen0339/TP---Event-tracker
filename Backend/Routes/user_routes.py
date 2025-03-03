import datetime
import os
from flask_restx import Namespace, Resource, fields
from flask import jsonify, request, make_response
import jwt
from Services import login_services
import logging

logging.basicConfig(level=logging.DEBUG)

# Brug en miljøvariabel i produktion
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")

# Create a Namespace for better organization
ns_events = Namespace('users', description='User-related operations')

# Define the input model for user creation
# Define the input model for user creation
user_creation_model = ns_events.model('UserCreate', {
    'username': fields.String(required=True, description='The username for the user'),
    'password': fields.String(required=True, description='The password for the user')
})

# Define input model for login
user_login_model = ns_events.model('UserLogin', {
    'username': fields.String(required=True, description='The username for the user'),
    'password': fields.String(required=True, description='The user password')
})

@ns_events.route('/user_create')
class UserCreate(Resource):
    def options(self):
        return {"message": "CORS preflight successful"}, 200

    @ns_events.expect(user_creation_model)  # Expecting the user creation model
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        try:
            result, status_code = login_services.user_create(username=username, password=password)
            return result, status_code
        except Exception as e:
            return {"error": str(e)}, 500

@ns_events.route('/user_login')
class UserLogin(Resource):
    def options(self):
        return {"message": "CORS preflight successful"}, 200

    @ns_events.expect(user_login_model)  # Expecting the login model
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        try:
            result, status_code = login_services.user_login(username=username, password=password)

            if status_code != 200:
                return result, status_code  # Return error response directly

            # Create response data
            response = make_response(jsonify({"message" : "Login successful", "username": username}))
            response.set_cookie(
                'token',
                result["token"],
                samesite='None',
                secure=True
            )

            return response

        except Exception as e:
            logging.error(f"Error while logging in user: {str(e)}")
            return {"error": str(e)}, 500

@ns_events.route('/user_change_password')
class UserChangePassword(Resource):
    def options(self):
        return {"message": "CORS preflight successful"}, 200

    def post(self):
        # Add logic for changing password here
        return jsonify({"message": "Change password endpoint"}), 200
    
@ns_events.route('/check')
class AuthCheck(Resource):
    def get(self):
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request cookies: {request.cookies}")
        
        token = request.cookies.get('token')
        logging.debug(f"Received token: {token}")  # Log token

        if not token:
            return make_response(jsonify({"authenticated": False, "error": "No token provided"}), 401)
        
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return make_response(jsonify({"authenticated": True, "username": decoded["username"]}), 200)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"authenticated": False, "error": "Session expired"}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({"authenticated": False, "error": "Invalid token"}), 401)