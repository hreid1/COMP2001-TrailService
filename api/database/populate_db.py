# create_db.py
from config import db, app
from models import Trail, Owner 

# Push the application context
with app.app_context():
    # Drop all of the existing database tables
    db.drop_all()
    # Create the database and the database tables
    db.create_all()

    # Add initial data
    initial_owners = [
        Owner(
            owner_name="John Doe",
            email="john.doe@example.com",
            is_admin=True
        ),
        Owner(
            owner_name="Jane Smith",
            email="jane.smith@example.com",
            is_admin=False
        )
    ]

    db.session.bulk_save_objects(initial_owners)
    db.session.commit()

    initial_trails = [
        Trail(
            name="Appalachian Trail",
            difficulty="Hard",
            location="Eastern United States",
            length=2190.0,
            elevation_gain=464000.0,
            owner_id=1  # Assuming John Doe is the owner
        ),
        Trail(
            name="Pacific Crest Trail",
            difficulty="Hard",
            location="Western United States",
            length=2650.0,
            elevation_gain=420000.0,
            owner_id=1  # Assuming John Doe is the owner
        ),
        Trail(
            name="John Muir Trail",
            difficulty="Moderate",
            location="California",
            length=211.0,
            elevation_gain=47000.0,
            owner_id=2  # Assuming Jane Smith is the owner
        )
    ]

    db.session.bulk_save_objects(initial_trails)
    db.session.commit()

    print("Database created and initial data added successfully!")