from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from api.database.config import db,ma

class LocationPoint(db.Model):
    __tablename__ = 'location_point'
    id = db.Column(db.Integer, primary_key=True)
    trailID = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)
    sequenceNumber = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    # Relationship with the Trail model
    trail = db.relationship('Trail', back_populates='location_points') 

class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    trailID = fields.Integer(required=True)
    latitude = fields.Decimal(as_string=True)
    longitude = fields.Decimal(as_string=True)
    sequenceNumber = fields.Integer()
    timestamp = fields.DateTime()

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)