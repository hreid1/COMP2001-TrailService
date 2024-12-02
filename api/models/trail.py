from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config import db, ma

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
        # One-to-many relationship with LocationPoint
    location_points = db.relationship('LocationPoint', back_populates='trail', cascade='all, delete-orphan')
    
        # Many-to-many relationship with TrailFeature through TrailFeatureJoin
    features = db.relationship('TrailFeature', secondary='trail_feature_join', back_populates='trails')
    
        # Foreign key relationships with other tables
    difficulty = db.relationship('Difficulty', back_populates='trails')
    route_type = db.relationship('RouteType', back_populates='trails')
    location = db.relationship('Location', back_populates='trails')
    owner = db.relationship('Owner', back_populates='trails')

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
    
    # Nested relationships
    location_points = fields.Nested('LocationPointSchema', many=True)  # Nested relationship with LocationPoint
    features = fields.Nested('TrailFeatureSchema', many=True)  # Nested relationship with TrailFeature
    difficulty = fields.Nested('DifficultySchema', many=False)  # Nested relationship with Difficulty
    route_type = fields.Nested('RouteTypeSchema', many=False)  # Nested relationship with RouteType
    location = fields.Nested('LocationSchema', many=False)  # Nested relationship with Location
    owner = fields.Nested('OwnerSchema', many=False)  # Nested relationship with Owner

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
