# populate_db.py
from config import db, app
from models import Trail, Owner, RouteType

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

    # Route Type
    route_types = [
        RouteType(route_type='Loop'),
        RouteType(route_type='Out and Back'),
        RouteType(route_type='Point to Point')
    ]

    # Add the data to the session and commit
    db.session.bulk_save_objects(route_types)
    db.session.commit()

    # Fetch the route types to get their IDs
    loop_route = RouteType.query.filter_by(route_type='Loop').first()
    out_and_back_route = RouteType.query.filter_by(route_type='Out and Back').first()
    point_to_point_route = RouteType.query.filter_by(route_type='Point to Point').first()

    initial_trails = [
        Trail(
            name="Appalachian Trail",
            difficulty="Hard",
            location="Eastern United States",
            length=2190.0,
            elevation_gain=464000.0,
            owner_id=1,  # Assuming John Doe is the owner
            route_id=point_to_point_route.route_id  # Assuming Point to Point route type
        ),
        Trail(
            name="Pacific Crest Trail",
            difficulty="Hard",
            location="Western United States",
            length=2650.0,
            elevation_gain=420000.0,
            owner_id=1,  # Assuming John Doe is the owner
            route_id=point_to_point_route.route_id  # Assuming Point to Point route type
        ),
        Trail(
            name="John Muir Trail",
            difficulty="Moderate",
            location="California",
            length=211.0,
            elevation_gain=47000.0,
            owner_id=2,  # Assuming Jane Smith is the owner
            route_id=out_and_back_route.route_id  # Assuming Out and Back route type
        )
    ]

    db.session.bulk_save_objects(initial_trails)
    db.session.commit()

    print("Database created and initial data added successfully!")