from flask import request, abort
import requests

AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

# Sample User Data
users = {
    "grace@plymouth.ac.uk": {"password": "ISAD123!", "role": "admin"},
    "ada@plymouth.ac.uk": {"password": "COMP2001!", "role": "user"},
    "tim@plymouth.ac.uk": {"password": "insecurePassword", "role": "user"}
}

def authenticate_request():
    auth_data = request.headers.get('Authorization')
    if not auth_data:
        abort(401, "No Authorization header")
    
    try:
        email, password = auth_data.split(':')
    except ValueError:
        abort(401, "Invalid Authorization header")

    # Check if the email exists in our hardcoded user data
    user = users.get(email)
    if not user or user['password'] != password:
        abort(401, "Invalid email or password")
    
    # Simulate a response to indicate successful authentication
    return {"email": email, "role": user['role'], "user_id": email}

def check_admin(user):
    if user['role'] != 'admin':
        abort(403, "User is not an admin")

def check_owner(user, trail):
    if user['user_id'] != trail['owner_id']:
        abort(403, "User is not the owner of the trail")
