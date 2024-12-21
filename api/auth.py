from flask import request, abort
import requests

AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

email = 'tim@plymouth.ac.uk'
password = 'COMP2001!'

credentials = {
    'email': email,
    'password': password
}

def authenticate_user(email, password):
    response = requests.post(AUTH_URL, json=credentials)
    if response.status_code != 200:
        try:
            json_response = response.json()
            print("Authenticated successfully", json_response)
        except requests.JSONDecodeError:
            print("Failed to authenticate", response.text)
    else:
        print(f"Authentication failed with status code {response.status_code}")
        print("Failed to authenticate", response.text)
        
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






