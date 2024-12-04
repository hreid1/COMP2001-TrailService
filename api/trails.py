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

def read_one(trail_id):
    trail = Trail.query.get(trail_id)
    if trail is not None:
        return trail_schema.jsonify(trail)
    else:
        abort(404, f"Trail with ID {trail_id} not found")

def read_all():
    trails = Trail.query.all()
    return trails_schema.jsonify(trails)

def create(trail):
    print("Called Create function of trail")
    #new_trail = trail_schema.load(trail, session=db.session)
    #db.session.add(new_trail)
    #b.session.commit()
    #return trail_schema.jsonify(new_trail), 201

def update(trail_id, trail):
    print("Called Update function of trail")
    #existing_trail = Trail.query.get(trail_id)
    #if existing_trail:
        #update_trail = trail_schema.load(trail, session=db.session)
        #existing_trail.name = update_trail.name
        #existing_trail.location = update_trail.location
        #existing_trail.length = update_trail.length
        #existing_trail.difficulty = update_trail.difficulty
        #db.session.merge(existing_trail)
        #db.session.commit()
        #return trail_schema.dump(existing_trail), 201
    #else:
        #abort(404, f"Trail with ID {trail_id} not found")

def delete(trail_id):
    print("Called Delete function of trail")
    #existing_trail = Trail.query.get(trail_id)
    #if existing_trail:
        #db.session.delete(existing_trail)
        #db.session.commit()
        #return make_response(f"Trail with ID {trail_id} successfully deleted", 204)
   #else:
        #abort(404, f"Trail with ID {trail_id} not found")