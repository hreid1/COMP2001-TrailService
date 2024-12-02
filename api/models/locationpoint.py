from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

from database import db, ma

class LocationPoint(db.Model):
    __tablename__ = 'location_point'
    id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    sequenceNumber = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')))

    # Relationships
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
    timestamp = fields.DateTime()

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)