from flask import abort, make_response
from config import db
from models import RouteType, route_type_schema, route_types_schema

def read_all():
    routetypes = RouteType.query.all()
    return route_type_schema.dump(routetypes)

def create(routetype):
    routeTypeName = routetype.get("routeTypeName")
    existing_routetype = RouteType.query.filter(RouteType.routeTypeName == routeTypeName).one_or_none()
    if existing_routetype is None:
        schema = route_type_schema.load(routetype, session=db.session)
        db.session.add(schema)
        db.session.commit()
        return route_type_schema.dump(schema), 201
    else:
        abort(409, f'RouteType {routeTypeName} exists already')

def read_one(routeTypeID):
    routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if routetype is not None:
        return route_type_schema.dump(routetype)
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')

def update(routeTypeID, routetype):
    update_routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if update_routetype is not None:
        schema = route_type_schema.load(routetype, session=db.session)
        schema.routeTypeID = update_routetype.routeTypeID
        db.session.merge(schema)
        db.session.commit()
        return route_type_schema.dump(schema), 200
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')

def delete(routeTypeID):
    routetype = RouteType.query.filter(RouteType.routeTypeID == routeTypeID).one_or_none()
    if routetype is not None:
        db.session.delete(routetype)
        db.session.commit()
        return make_response(f'RouteType {routeTypeID} successfully deleted', 200)
    else:
        abort(404, f'RouteType not found for Id: {routeTypeID}')