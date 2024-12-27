from flask import abort, make_response, jsonify, Request, request
import requests
from config import db
from models import Owner, Trail
import base64

# Owner
    # owner_id
    # owner_name
    # email
    # role -> admin or user

    # Sample Data -> Assigned role by me
        # owner_name: "Grace Hopper", email: "grace@plymouth.ac.uk", role: "admin"
        # owner_name: "Tim Berners-Lee", email: "tim@plymouth.ac.uk, role; "user"

    # API Data -> No role assigned
        # username: "Grace Hopper", email: "grace@plymouth.ac.uk", password: "ISAD123!"
        # username: "Tim Berners-Lee", email: "tim@plymouth.ac.uk", password: "COMP2001!"
        # username: "Ada Lovelace", email: "ada@plymouth.ac.uk", password: "insecurePassword"

# Steps
    # Get owner from DB and return the role

    # Then authenticate against the API to prove the user exists

# Authentication details -> No assigned role, simply checks if user exists
auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

def get_owner_by_email(email):
    owner = db.session.query(Owner).filter_by(email=email).first()
    return owner

# Authenticate the user against the external API
def authenticate_user(email, password):
    credentials = {
        'email': email,
        'password': password
    }

    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:
        try:
            json_response = response.json()  # Parse the JSON response
            print("Authenticated successfully:", json_response)
            return True
        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content:")
            print(response.text)
            return False
    else:
        print(f"Authentication failed with status code {response.status_code}")
        print("Response content:", response.text)
        return False
