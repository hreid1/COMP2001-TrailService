from flask import abort, make_response, jsonify, request

from config import db
from models import Trail, trail_schema, trails_schema

# CRUD functions
    # Create
    # Read
        # Read one
        # Read all
    # Update
    # Delete
        # Can only delete trail if admin/author of trail
# Need to check user is admin before anything


def read_all():
    trails = Trail.query.all()
    return jsonify(trails_schema.dump(trails))

def create():
    print("Called Create function of trail")
    trail = request.get_json()
    new_trail = trail_schema.load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.jsonify(new_trail), 201

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
    existing_trail = Trail.query.get(trail_id)
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail with ID {trail_id} successfully deleted", 204)
    else:
        abort(404, f"Trail with ID {trail_id} not found")