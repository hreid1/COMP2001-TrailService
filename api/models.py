# models.py
from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from marshmallow import fields

# Models

# Trail
    # trail_id
    # name
    # difficulty
    # location
    # length
    # elevation_gain
    # description
    # owner_id
    # route_id

# Owner
    # owner_id
    # owner_name
    # email
    # role

# RouteType
    # route_id
    # route_type

# TrailFeature JOIN TABLE Trail -> Feature
    # trail_id
    # feature_id

# Feature
    # feature_id
    # feature_name

# LocationPoint
    # location_point_id
    # longitude
    # latitude
    # description

# TrailPoints (JOIN TABLE) Trail -> LocationPoint
    # trail_id -> Trail.trail_id
    # location_point_id -> LocationPoint.location_point_id
    # sequenceNumber


class TrailPoints(db.Model):
    __tablename__ = 'trail_points'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    location_point_id = db.Column(db.Integer, db.ForeignKey('CW2.location_point.location_point_id'), primary_key=True)
    sequence_number = db.Column(db.Integer, nullable=False)

class TrailPointsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoints
        load_instance = True
        sqla_session = db.session

    trail_id = fields.Integer(required=True)
    location_point_id = fields.Integer(required=True)
    sequence_number = fields.Integer(required=True)

class TrailFeature(db.Model):
    __tablename__ = 'trail_features'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('CW2.feature.feature_id'), primary_key=True)

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

    trail_id = fields.Integer(required=True)
    feature_id = fields.Integer(required=True)

class Trail(db.Model):
    __tablename__ = 'trails'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('CW2.owners.owner_id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('CW2.route_type.route_id'), nullable=False)

    trail_features = db.relationship(TrailFeature, backref='trails_trail_features', single_parent=True)
    trail_points = db.relationship(TrailPoints, backref='trails_trail_points', single_parent=True)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    owner_id = fields.Integer(required=True)
    route_id = fields.Integer(required=True)

    # Nested fields for trail_points and trail_features
    trail_points = fields.Nested('TrailPointsSchema', many=True, required=False)
    trail_features = fields.Nested('TrailFeatureSchema', many=True, required=False)


class Feature(db.Model):
    __tablename__ = 'feature'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(50), nullable=False)

    trail_features = db.relationship(TrailFeature, backref='feature_trail_features', single_parent=True)

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session

    feature_id = fields.Integer(dump_only=True)
    feature_name = fields.String(required=True)

class LocationPoint(db.Model):
    __tablename__ = 'location_point'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    location_point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    trail_points = db.relationship(TrailPoints, backref='location_point_trail_points', single_parent=True)

class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

class Owner(db.Model):
    __tablename__ = 'owners'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    owner_id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.Boolean, nullable=False)

    trails = db.relationship('Trail', backref='owners', lazy=True)

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session

    owner_id = fields.Integer(dump_only=True)
    owner_name = fields.String(required=True)
    email = fields.String(required=True)
    role = fields.Boolean(required=True)

class RouteType(db.Model):
    __tablename__ = 'route_type'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    route_id = db.Column(db.Integer, primary_key=True)
    route_type = db.Column(db.String(50), nullable=False)

    trails = db.relationship('Trail', backref='route_type', lazy=True)

class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

    route_id = fields.Integer(dump_only=True)
    route_type = fields.String(required=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)

route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)

trail_points_schema = TrailPointsSchema()

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

trail_feature_schema = TrailFeatureSchema()










