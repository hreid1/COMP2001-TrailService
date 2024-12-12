from flask import abort, make_response, jsonify, request
from config import db
from models import RouteType, route_type_schema, route_types_schema


# CRUD Operations for Route Types
     # Create
        # Read    
            # Read one
            # Read all
        # Update
        # Delete

def read_one(route_type_id):
    route_type = RouteType.query.get(route_type_id)
    if route_type is not None:
        return route_type_schema.jsonify(route_type)
    else:
        abort(404, f"Route Type with ID {route_type_id} not found")

def read_all():
    route_types = RouteType.query.all()
    return route_types_schema.jsonify(route_types)

def create(route_type):
    new_route_type = route_type_schema.load(route_type, session=db.session)
    db.session.add(new_route_type)
    db.session.commit()
    return route_type_schema.jsonify(new_route_type), 201

def update(route_type_id, route_type):
    existing_route_type = RouteType.query.get(route_type_id)
    if existing_route_type:
        update_route_type = route_type_schema.load(route_type, session=db.session)
        existing_route_type.route_type = update_route_type.route_type
        db.session.merge(existing_route_type)
        db.session.commit()
        return route_type_schema.dump(existing_route_type), 201
    else:
        abort(404, f"Route Type with ID {route_type_id} not found")

def delete(route_type_id):
    existing_route_type = RouteType.query.get(route_type_id)
    if existing_route_type:
        db.session.delete(existing_route_type)
        db.session.commit()
        return make_response(f"Route Type with ID {route_type_id} successfully deleted", 204)
    else:
        abort(404, f"Route Type with ID {route_type_id} not found")

        
