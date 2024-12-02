from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from api.database.config import db, ma

class TrailFeature(db.Model):
    __tablename__ = 'trail_feature'
    id = db.Column(db.Integer, primary_key=True)
    featureName = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    # Relationship with TrailFeatureJoin (many-to-many relationship)
    trails = db.relationship('Trail', secondary='trail_feature_join', back_populates='features')

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    featureName = fields.String(required=True)
    timestamp = fields.DateTime()

trail_feature_schema = TrailFeatureSchema()
trail_features_schema = TrailFeatureSchema(many=True)
