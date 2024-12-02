from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

from database import db, ma

class TrailFeatureJoin(db.Model):
    __tablename__ = 'trail_feature_join'
    id = db.Column(db.Integer, primary_key=True)
    trailID = db.Column(db.Integer, db.ForeignKey('trail.id'))
    featureID = db.Column(db.Integer, db.ForeignKey('trail_feature.id'))

    # Relationship with Trail
    trail = db.relationship('Trail', back_populates='trail_feature_joins')
    feature = db.relationship('TrailFeature', back_populates='trail_features')

class TrailFeatureJoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeatureJoin
        load_instance = True
        sqla_session = db.session

    trailID = fields.Integer(required=True)
    featureID = fields.Integer(required=True)

trail_feature_join_schema = TrailFeatureJoinSchema()
trail_feature_joins_schema = TrailFeatureJoinSchema(many=True)
