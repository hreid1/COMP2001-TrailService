from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from api.database.config import db,ma

class TrailFeatureJoin(db.Model):
    __tablename__ = 'trail_feature_join'
    trailID = db.Column(db.Integer, db.ForeignKey('trail.id'), primary_key=True)
    featureID = db.Column(db.Integer, db.ForeignKey('trail_feature.id'), primary_key=True)

    # Relationships
    trail = db.relationship('Trail', back_populates='features')
    feature = db.relationship('TrailFeature', back_populates='trails')

class TrailFeatureJoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeatureJoin
        load_instance = True
        sqla_session = db.session

    trailID = fields.Integer()
    featureID = fields.Integer()

trail_feature_join_schema = TrailFeatureJoinSchema()
trail_feature_joins_schema = TrailFeatureJoinSchema(many=True)
