from flask import abort, make_response
from api.database.config import db
from models import Location, location_schema, locations_schema

def read_all():
    locations = Location.query.order_by(Location.locationName).all()
    locations = locations_schema.dump(locations)
    return locations

def read_one(location_id):
    location = Location.query.filter(Location.id == location_id).one_or_none()
    if location is not None:
        location = location_schema.dump(location)
    else:
        abort(404, f'Location not found for Id: {location_id}')
    return location

def create(location):
    locationName = location.get('locationName')
    existing_location = Location.query.filter(Location.locationName == locationName).one_or_none()
    if existing_location is None:
        new_location = Location(locationName=locationName)
        db.session.add(new_location)
        db.session.commit()
        return location_schema.dump(new_location), 201
    else:
        abort(409, f'Location {locationName} exists already')

def update(location_id, location):
    update_location = Location.query.filter(Location.id == location_id).one_or_none()
    if update_location is not None:
        location_schema.load(location, session=db.session)
        db.session.commit()
        return location_schema.dump(update_location), 200
    else:
        abort(404, f'Location not found for Id: {location_id}')

def delete(location_id):
    location = Location.query.filter(Location.id == location_id).one_or_none()
    if location is not None:
        db.session.delete(location)
        db.session.commit()
        return make_response(f'Location {location_id} deleted', 204)
    else:
        abort(404, f'Location not found for Id: {location_id}')

        