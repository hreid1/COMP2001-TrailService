from datetime import datetime
from flask import abort, make_response
from config import db
from models import Trail, trail_schema, trails_schema

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def read_all():
    trail = Trail.query.all()
    return trails_schema.dump(trail)

def read_one(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        abort(404)
    return trail_schema.dump(trail)

def create(trail):
    trail = Trail(
        trailName=trail.get("trailName"),
        rating=trail.get("rating"),
        difficultyID=trail.get("difficultyID"),
        routeTypeID=trail.get("routeTypeID"),
        locationID=trail.get("locationID"),
        trailDescription=trail.get("trailDescription"),
        trailDistance=trail.get("trailDistance"),
        trailElevationGain=trail.get("trailElevationGain"),
        averageTimeToComplete=trail.get("averageTimeToComplete"),
        ownerID=trail.get("ownerID"),
    )
    db.session.add(trail)
    db.session.commit()
    return trail_schema.dump(trail), 201

def update(trail_id, trail):
    trail_to_update = Trail.query.get(trail_id)
    if not trail_to_update:
        abort(404)
    trail_to_update.trailName = trail.get("trailName")
    trail_to_update.rating = trail.get("rating")
    trail_to_update.difficultyID = trail.get("difficultyID")
    trail_to_update.routeTypeID = trail.get("routeTypeID")
    trail_to_update.locationID = trail.get("locationID")
    trail_to_update.trailDescription = trail.get("trailDescription")
    trail_to_update.trailDistance = trail.get("trailDistance")
    trail_to_update.trailElevationGain = trail.get("trailElevationGain")
    trail_to_update.averageTimeToComplete = trail.get("averageTimeToComplete")
    trail_to_update.ownerID = trail.get("ownerID")
    trail_to_update.updated_at = get_timestamp()
    db.session.commit()
    return trail_schema.dump(trail_to_update)

def delete(trail_id):
    trail = Trail.query.get(trail_id)
    if not trail:
        abort(404)
    db.session.delete(trail)
    db.session.commit()
    return make_response("", 204)
