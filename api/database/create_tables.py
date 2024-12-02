
from datetime import datetime
from config import app, db
from models import Owner

# Sample data for the Owner table
OWNERS_DATA = [
    {
        "ownerName": "Grace Hopper",
        "email": "grace.hopper@example.com",
        "isAdmin": True
    },
    {
        "ownerName": "Tim Berners-Lee",
        "email": "tim.lee@example.com",
        "isAdmin": False
    },
    {
        "ownerName": "Ada Lovelace",
        "email": "ada.lovelace@example.com",
        "isAdmin": False
    },
]

with app.app_context():
    # Drop all existing tables and recreate them
    db.drop_all()
    db.create_all()

    # Add the sample owners to the database
    for data in OWNERS_DATA:
        new_owner = Owner(
            ownerName=data.get("ownerName"),
            email=data.get("email"),
            isAdmin=data.get("isAdmin")
        )
        db.session.add(new_owner)

    # Commit the changes to the database
    db.session.commit()

    print("Owner table created and data added successfully!")
