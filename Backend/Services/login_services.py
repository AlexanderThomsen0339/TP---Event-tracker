from Reposetories import user_reposetory
import bcrypt
import jwt
import datetime
import os
from flask import jsonify, make_response, request

# Brug en miljøvariabel i produktion
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")

def user_login(username, password):
    user = user_reposetory.get_user_by_name(username)
    if not user:
        return {"error": "User not found"}, 404  

    stored_password = user["password"]
    print("Brugerens password fra DB:", stored_password)
    print("Type af stored_password:", type(stored_password))
    if not bcrypt.checkpw(password.encode(), stored_password.encode()):
        return {"error": "Incorrect password"}, 401  

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token}, 200

def check_auth():
    token = request.cookies.get("token")  # Rettet fra "auth_token" til "token"
    if not token:
        return jsonify({"authenticated": False}), 401  

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"authenticated": True, "username": decoded["username"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"authenticated": False, "error": "Session expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"authenticated": False, "error": "Invalid token"}), 401
    
def user_create(username, password):
    if not username or not password:
        return {"error": "Username and password are required"}, 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    

    try:
        user_reposetory.create_user(username, hashed_password)
        return {"message": "User created successfully"}, 201
    except Exception as e:
        return {"error": f"Error: {str(e)}"}, 500