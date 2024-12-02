from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from database import db, ma

class RouteType(db.Model):
    __tablename__ = 'route_type'
    routeTypeID = db.Column(db.Integer, primary_key=True)
    routeTypeName = db.Column(db.String(255), nullable=False, unique=True)

    # Relationship with Trail
    #trails = db.relationship('Trail', back_populates='route_type')

class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

    routeTypeID = fields.Integer(dump_only=True)
    routeTypeName = fields.String(required=True)

route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)
