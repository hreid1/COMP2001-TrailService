from flask import abort, make_response
from api.database.config import db
from models import Trail, trail_schema, trails_schema

# Get all trails
def read_all():
    trails = Trail.query.order_by(Trail.trailName).all()
    return trails_schema.dump(trails)  # Correct schema for multiple items

# Get one trail by ID
def read_one(trail_id):
    trail = Trail.query.filter(Trail.trailID == trail_id).one_or_none()
    if trail:
        return trail_schema.dump(trail)
    else:
        abort(404, f'Trail not found for Id: {trail_id}')

# Create a new trail
def create(trail):
    trailName = trail.get('trailName')
    existing_trail = Trail.query.filter(Trail.trailName == trailName).one_or_none()
    if existing_trail is None:
        # Expand creation logic to include all relevant fields
        new_trail = Trail(
            trailName=trailName,
            trailDescription=trail.get('trailDescription'),
            rating=trail.get('rating'),
            difficultyID=trail.get('difficultyID'),
            routeTypeID=trail.get('routeTypeID'),
            locationID=trail.get('locationID'),
            trailDistance=trail.get('trailDistance'),
            trailElevationGain=trail.get('trailElevationGain'),
            averageTimeToComplete=trail.get('averageTimeToComplete'),
            ownerID=trail.get('ownerID')
        )
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201  # Return created trail
    else:
        abort(409, f'Trail {trailName} already exists')

# Update an existing trail
def update(trail_id, trail):
    update_trail = Trail.query.filter(Trail.trailID == trail_id).one_or_none()
    if update_trail:
        # Manually update fields directly
        update_trail.trailName = trail.get('trailName', update_trail.trailName)
        update_trail.trailDescription = trail.get('trailDescription', update_trail.trailDescription)
        update_trail.rating = trail.get('rating', update_trail.rating)
        update_trail.difficultyID = trail.get('difficultyID', update_trail.difficultyID)
        update_trail.routeTypeID = trail.get('routeTypeID', update_trail.routeTypeID)
        update_trail.locationID = trail.get('locationID', update_trail.locationID)
        update_trail.trailDistance = trail.get('trailDistance', update_trail.trailDistance)
        update_trail.trailElevationGain = trail.get('trailElevationGain', update_trail.trailElevationGain)
        update_trail.averageTimeToComplete = trail.get('averageTimeToComplete', update_trail.averageTimeToComplete)
        update_trail.ownerID = trail.get('ownerID', update_trail.ownerID)
        
        db.session.commit()
        return trail_schema.dump(update_trail), 200  # Return updated trail
    else:
        abort(404, f'Trail not found for Id: {trail_id}')

# Delete a trail
def delete(trail_id):
    trail = Trail.query.filter(Trail.trailID == trail_id).one_or_none()
    if trail:
        db.session.delete(trail)
        db.session.commit()
        return make_response(f'Trail {trail_id} deleted', 204)
    else:
        abort(404, f'Trail not found for Id: {trail_id}')
