from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

from database import db, ma

class LocationPoint(db.Model):
    __tablename__ = 'location_point'
    pointID = db.Column(db.Integer, primary_key=True)
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))

    trail = db.relationship('Trail', back_populates='location_points')

class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    trail_id = fields.Integer()
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    sequenceNumber = fields.Integer(required=True)
    timestamp = fields.DateTime(dump_only=True)

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)