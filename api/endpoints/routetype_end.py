from flask import abort, make_response, jsonify, request
from database import db
from models import RouteType, route_type_schema, route_types_schema

# Get all route types
def read_all():
    route_types = RouteType.query.order_by(RouteType.routeTypeName).all()
    return route_types_schema.dump(route_types)

# Get one route type by ID
def read_one(route_type_id):
    route_type = RouteType.query.filter(RouteType.routeTypeID == route_type_id).one_or_none()
    if route_type:
        return route_type_schema.dump(route_type)
    else:
        abort(404, description=f'RouteType not found for Id: {route_type_id}')

# Create a new route type
def create():
    route_type_data = request.get_json()
    routeTypeName = route_type_data.get('routeTypeName')
    
    if not routeTypeName:
        abort(400, description='Route type name is required')

    existing_route_type = RouteType.query.filter(RouteType.routeTypeName == routeTypeName).one_or_none()
    
    if existing_route_type is None:
        new_route_type = RouteType(routeTypeName=routeTypeName)
        db.session.add(new_route_type)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error creating route type: {str(e)}')
        return route_type_schema.dump(new_route_type), 201
    else:
        abort(409, description=f'Route type with name {routeTypeName} already exists')

# Update an existing route type
def update(route_type_id):
    route_type_data = request.get_json()
    route_type = RouteType.query.filter(RouteType.routeTypeID == route_type_id).one_or_none()
    
    if route_type:
        route_type.routeTypeName = route_type_data.get('routeTypeName', route_type.routeTypeName)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error updating route type: {str(e)}')
        return route_type_schema.dump(route_type)
    else:
        abort(404, description=f'RouteType not found for Id: {route_type_id}')

# Delete a route type
def delete(route_type_id):
    route_type = RouteType.query.filter(RouteType.routeTypeID == route_type_id).one_or_none()
    
    if route_type:
        try:
            db.session.delete(route_type)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error deleting route type: {str(e)}')
        return make_response(jsonify({"message": "RouteType deleted successfully"}), 204)
    else:
        abort(404, description=f'RouteType not found for Id: {route_type_id}')
