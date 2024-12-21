from flask import request, abort
import requests

AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'
        
def authenticate_request():
    auth_data = request.headers.get('Authorization')
    if not auth_data:
        abort(401, "No Authorization header")
    try:
        email, password = auth_data.split(':')
    except ValueError:
        abort(401, "Invalid Authorization header")

    credentials = {
        'email': email,
        'password': password
    }
    response = requests.post(AUTH_URL, json=credentials)

    if response.status_code == 200:
        try:
            return response.json()
        except requests.JSONDecodeError:
            abort(401, "Failed to authenticate")
    else:
        abort(401, "Failed to authenticate, invalid email or password")
    
def check_admin(user):
    if user['role'] != 'admin':
        abort(403, "User is not an admin")

def check_owner(user, trail):
    if user['user_id'] != trail['owner_id']:
        abort(403, "User is not the owner of the trail")






