from flask import abort, make_response
from api.database.config import db
from models import LocationPoint, location_point_schema, location_points_schema

# Get all location points
def read_all():
    location_points = LocationPoint.query.all()
    return location_points_schema.dump(location_points)  # Serialize all location points

# Get one location point by ID
def read_one(location_point_id):
    location_point = LocationPoint.query.filter(LocationPoint.locationPointID == location_point_id).one_or_none()
    if location_point:
        return location_point_schema.dump(location_point)  # Serialize the single location point
    else:
        abort(404, f'LocationPoint not found for Id: {location_point_id}')

# Create a new location point
def create(location_point):
    trailID = location_point.get('trailID')
    latitude = location_point.get('latitude')
    longitude = location_point.get('longitude')
    sequenceNumber = location_point.get('sequenceNumber')

    new_location_point = LocationPoint(
        trailID=trailID,
        latitude=latitude,
        longitude=longitude,
        sequenceNumber=sequenceNumber
    )

    db.session.add(new_location_point)
    db.session.commit()
    return location_point_schema.dump(new_location_point), 201  # Return created location point

# Update an existing location point
def update(location_point_id, location_point):
    update_location_point = LocationPoint.query.filter(LocationPoint.locationPointID == location_point_id).one_or_none()
    if update_location_point:
        # Manually update fields directly
        update_location_point.latitude = location_point.get('latitude', update_location_point.latitude)
        update_location_point.longitude = location_point.get('longitude', update_location_point.longitude)
        update_location_point.sequenceNumber = location_point.get('sequenceNumber', update_location_point.sequenceNumber)
        update_location_point.trailID = location_point.get('trailID', update_location_point.trailID)

        db.session.commit()
        return location_point_schema.dump(update_location_point), 200  # Return updated location point
    else:
        abort(404, f'LocationPoint not found for Id: {location_point_id}')

# Delete a location point
def delete(location_point_id):
    location_point = LocationPoint.query.filter(LocationPoint.locationPointID == location_point_id).one_or_none()
    if location_point:
        db.session.delete(location_point)
        db.session.commit()
        return make_response(f'LocationPoint {location_point_id} deleted', 204)  # No content response
    else:
        abort(404, f'LocationPoint not found for Id: {location_point_id}')
