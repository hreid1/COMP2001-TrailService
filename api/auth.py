import requests
from flask import request, Request
from models import Owner  # Assuming you have a model defined for the Owner table
from config import db

# Define the authentication URL
auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

# is_owner_admin
def is_admin(owner):
    return owner.role == 'admin'

def get_owner(req: Request):
    email = request.headers.get('email')
    owner = Owner.query.filter_by(email=email).one_or_none()
    return owner

def owner_exists(req: Request):
    email = request.headers.get('email')
    password = req.headers.get('password')

    if email is None or password is None:
        return False
    
    body = {
        'email': email,
        'password': password
    }

    response = requests.post(auth_url, json=body)

    response = response.json()

    return response[1] == 'True'