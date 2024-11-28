from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from config import db, ma

class Trail(db.Model):
    __tablename__ = 'trail'
    id = db.Column(db.Integer, primary_key=True)
    trailName = db.Column(db.String(255), nullable=False, unique=True)
    rating = db.Column(db.Numeric(3, 2), CheckConstraint('rating >= 0 AND rating <= 5'))
    difficultyID = db.Column(db.Integer, db.ForeignKey('difficulty.difficultyID'))
    routeTypeID = db.Column(db.Integer, db.ForeignKey('route_type.routeTypeID'))
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    trailDescription = db.Column(db.Text)
    trailDistance = db.Column(db.Numeric(6, 2))
    trailElevationGain = db.Column(db.Numeric(6, 2))
    averageTimeToComplete = db.Column(db.Numeric(5, 2))
    ownerID = db.Column(db.Integer, db.ForeignKey('owner.ownerID'))
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    trailName = fields.String(required=True)
    rating = fields.Decimal(as_string=True)
    difficultyID = fields.Integer()
    routeTypeID = fields.Integer()
    locationID = fields.Integer()
    trailDescription = fields.String()
    trailDistance = fields.Decimal(as_string=True)
    trailElevationGain = fields.Decimal(as_string=True)
    averageTimeToComplete = fields.Decimal(as_string=True)
    ownerID = fields.Integer()
    timestamp = fields.DateTime()

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)