from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from config import db, ma


class Location(db.Model):
    __tablename__ = 'location'
    locationID = db.Column(db.Integer, primary_key=True)
    locationName = db.Column(db.String(255), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session

    locationID = fields.Integer(dump_only=True)
    locationName = fields.String(required=True)
    timestamp = fields.DateTime()

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)