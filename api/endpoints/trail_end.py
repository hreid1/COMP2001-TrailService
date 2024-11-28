from flask import abort, make_response

from config import db
from models import Trail, trail_schema, trails_schema

def read_all():
    trails = Trail.query.order_by(Trail.trailName).all()
    trails = trails_schema.dump(trails)
    return trails

def read_one(trail_id):
    trail = Trail.query.filter(Trail.id == trail_id).one_or_none()
    if trail is not None:
        trail = trail_schema.dump(trail)
    else:
        abort(404, f'Trail not found for Id: {trail_id}')
    return trail

def create(trail):
    trailName = trail.get('trailName')
    existing_trail = Trail.query.filter(Trail.trailName == trailName).one_or_none()
    if existing_trail is None:
        new_trail = Trail(trailName=trailName)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(409, f'Trail {trailName} exists already')

def update(trail_id, trail):
    update_trail = Trail.query.filter(Trail.id == trail_id).one_or_none()
    if update_trail is not None:
        trail_schema.load(trail, session=db.session)
        db.session.commit()
        return trail_schema.dump(update_trail), 200
    else:
        abort(404, f'Trail not found for Id: {trail_id}')

def delete(trail_id):
    trail = Trail.query.filter(Trail.id == trail_id).one_or_none()
    if trail is not None:
        db.session.delete(trail)
        db.session.commit()
        return make_response(f'Trail {trail_id} deleted', 204)
    else:
        abort(404, f'Trail not found for Id: {trail_id}')