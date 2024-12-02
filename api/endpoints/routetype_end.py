from flask import abort, make_response
from api.database.config import db
from models import RouteType, route_type_schema, route_types_schema

# Get all route types
def read_all():
    routetypes = RouteType.query.all()
    return route_types_schema.dump(routetypes)  # Correct schema to handle multiple items

# Create a new route type
def create(routetype):
    routeTypeName = routetype.get("routeTypeName")
    if not routeTypeName:
        abort(400, description="Route Type Name is required")

    existing_routetype = RouteType.query.filter(RouteType.routeTypeName == routeTypeName).one_or_none()
    if existing_routetype is None:
        new_routetype = RouteType(routeTypeName=routeTypeName)
        db.session.add(new_routetype)
        db.session.commit()
        return route_type_schema.dump(new_routetype), 201  # Return created route type
    else:
        abort(409, f'RouteType {routeTypeName} already exists')

# Get one route type by ID
def read_one(routeTypeID):
    routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if routetype:
        return route_type_schema.dump(routetype)
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')

# Update an existing route type
def update(routeTypeID, routetype):
    update_routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if update_routetype:
        # Manually update fields instead of using schema load
        update_routetype.routeTypeName = routetype.get("routeTypeName", update_routetype.routeTypeName)
        db.session.commit()
        return route_type_schema.dump(update_routetype), 200  # Return updated route type
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')

# Delete a route type
def delete(routeTypeID):
    routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if routetype:
        db.session.delete(routetype)
        db.session.commit()
        return make_response(f'RouteType {routeTypeID} successfully deleted', 200)
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')
