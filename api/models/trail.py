from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import db, ma
from .trailfeaturejoin import TrailFeatureJoin  # Import TrailFeatureJoin

class Trail(db.Model):
    __tablename__ = 'trail'
    
    # Primary Fields
    id = db.Column(db.Integer, primary_key=True)
    trailName = db.Column(db.String(255), nullable=False, unique=True)
    rating = db.Column(db.Numeric(3, 2), CheckConstraint('rating >= 0 AND rating <= 5'))
    trailDescription = db.Column(db.Text)
    trailDistance = db.Column(db.Numeric(6, 2))
    trailElevationGain = db.Column(db.Numeric(6, 2))
    averageTimeToComplete = db.Column(db.Numeric(5, 2))
    
    # Foreign Keys
    difficultyID = db.Column(db.Integer, db.ForeignKey('difficulty.difficultyID'))
    routeTypeID = db.Column(db.Integer, db.ForeignKey('route_type.routeTypeID'))
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    ownerID = db.Column(db.Integer, db.ForeignKey('owner.ownerID'))
    
    # Timestamp
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    # Relationships
    features = relationship('TrailFeatureJoin', backref='trail')
    location_points = db.relationship('LocationPoint', back_populates='trail')  # Use deferred relationship

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    trailName = fields.String(required=True)
    rating = fields.Decimal()
    trailDescription = fields.String()
    trailDistance = fields.Decimal()
    trailElevationGain = fields.Decimal()
    averageTimeToComplete = fields.Decimal()
    difficultyID = fields.Integer()
    routeTypeID = fields.Integer()
    locationID = fields.Integer()
    ownerID = fields.Integer()
    timestamp = fields.DateTime()

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
