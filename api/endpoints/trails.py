from flask import abort, make_response, jsonify, request

from config import db
from models import Trail, trail_schema, trails_schema, location_point_schema, LocationPoint
from auth import authenticate_user

# Trail
    # trail_id
    # name
    # difficulty
    # location
    # length
    # elevation_gain
    # description
    # owner_id
    # route_id

    # Relationships
    # trail_points = db.relationship(TrailPoints, backref='trails_trail_points', single_parent=True)


# CRUD functions
    # Create
    # Read
        # Read one
            # Need to return associated RouteType, Owner
                # Via JOIN TABLES
            # Tables
                # Owner (owners)
                    # owner_id
                    # owner_name
                    # email
                    # role
                # RouteType (route_type)
                    # route_type_id
                    # route_type
                # TrailPoints (trail_points) JOIN TABLE
                    # trail_id
                    # location_point_id
                    # sequence_number
                # LocationPoint (location_point)
                    # location_point_id
                    # longitude
                    # latitude
                    # description
        # Read all
    # Update
    # Delete
        # Can only delete trail if admin/author of trail
# Need to check user is admin before anything
    # via auth.py
        #


def read_all():
    trails = Trail.query.all()
    return jsonify(trails_schema.dump(trails))

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    return jsonify({
        "trail": trail_schema.dump(trail),
        "route_type": trail.route_type.route_type,
        "owner": trail.owners.owner_name,
        "trail_points": [
            {
                "location_point": location_point_schema.dump(
                    LocationPoint.query.get(trail_point.location_point_id)
                ),
                "sequence_number": trail_point.sequence_number
            }
            for trail_point in trail.trail_points
        ]
    })


def create():
    print("Called Create function of trail")
    trail = request.get_json()
    new_trail = trail_schema.load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.jsonify(new_trail), 201

    # neeed to add trail_points
    # need to add trail_features

def update(trail_id):
    print("Called Update function of trail")
    trail = request.get_json()
    existing_trail = Trail.query.get(trail_id)
    if existing_trail:
        update_trail = trail_schema.load(trail, session=db.session)
        existing_trail.name = update_trail.name
        existing_trail.difficulty = update_trail.difficulty
        existing_trail.location = update_trail.location
        existing_trail.length = update_trail.length
        existing_trail.elevation_gain = update_trail.elevation_gain
        existing_trail.description = update_trail.description
        existing_trail.owner_id = update_trail.owner_id
        existing_trail.route_id = update_trail.route_id
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with ID {trail_id} not found")

def delete(trail_id):
    print("Called Delete function of trail")
    # Authenticate the user
    user_data = authenticate_user(request.headers.get('Authorization'))
    if user_data is None:
        abort(401, "Unauthorized access")

    # Check if user is admin or the owner of the trail
    existing_trail = Trail.query.get(trail_id)
    if existing_trail:
        if user_data['role'] != 'admin' and user_data['user_id'] != existing_trail.owner_id:
            abort(403, "You do not have permission to delete this trail")

        # Proceed with deletion if authorized
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail with ID {trail_id} successfully deleted", 204)
    else:
        abort(404, f"Trail with ID {trail_id} not found")