# models.py
from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from marshmallow import fields

# Models and Schemas

# Owner
    # owner_id
    # owner_name
    # email
    # is_admin

# Trail
    # trail_id
    # name
    # difficulty
    # location
    # length
    # elevation_gain
    # owner_id
    # route_id

# RouteType
    # route_id
    # route_type

# TrailFeature (JOIN TABLE) Trail and Feature
    # trail_id
    # feature_id

# Feature
    # feature_id
    # feature_name

# TrailPoints (JOIN TABLE) Trail and LocationPoint
    # trail_id
    # location_point_id
    # sequence_number

# LocationPoint
    # location_point_id
    # longitude
    # latitude

# Owner Model
class Owner(db.Model):
    __tablename__ = 'owners'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    trails = db.relationship('Trail', backref='owner', single_parent=True)

# Owner Schema
class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session

# RouteType Model
class RouteType(db.Model):
    __tablename__ = 'route_types'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_type = db.Column(db.String(50), nullable=False)

    trails = db.relationship('Trail', back_populates='route_type')

# RouteType Schema
class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

# Trail Model
class Trail(db.Model):
    __tablename__ = 'trails'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    elevation_gain = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('CW2.owners.owner_id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('CW2.route_types.route_id'), nullable=False)

    # Relationships
    owner = db.relationship('Owner', back_populates='trails')
    route_type = db.relationship('RouteType', back_populates='trails')
    trail_features = db.relationship('TrailFeature', back_populates='trail', cascade="all, delete, delete-orphan")
    location_points = db.relationship('TrailPoints', back_populates='trail', cascade="all, delete, delete-orphan")

# Trail Schema
class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        include_fk = True

# TrailFeature Model
class TrailFeature(db.Model):
    __tablename__ = 'trail_features'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('CW2.features.feature_id'), primary_key=True)

    # Relationships
    trail = db.relationship('Trail', back_populates='trail_features')
    feature = db.relationship('Feature', back_populates='trail_features')

# TrailFeature Schema
class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

# Feature Model
class Feature(db.Model):
    __tablename__ = 'features'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    feature_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature_name = db.Column(db.String(100), nullable=False)

    # Relationships
    trail_features = db.relationship('TrailFeature', back_populates='feature')

# Feature Schema
class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session

    trail_features = fields.Nested('TrailFeatureSchema', many=True)

# TrailPoints Model
class TrailPoints(db.Model):
    __tablename__ = 'trail_points'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    location_point_id = db.Column(db.Integer, db.ForeignKey('CW2.location_points.location_point_id'), primary_key=True)
    sequence_number = db.Column(db.Integer, nullable=False)

    # Relationships
    trail = db.relationship('Trail', back_populates='location_points')
    location_point = db.relationship('LocationPoint', back_populates='trail_points')

# TrailPoints Schema
class TrailPointsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoints
        load_instance = True
        sqla_session = db.session

# LocationPoint Model
class LocationPoint(db.Model):
    __tablename__ = 'location_points'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    location_point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Relationships
    trail_points = db.relationship('TrailPoints', back_populates='location_point')

# LocationPoint Schema
class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

    trail_points = fields.Nested('TrailPointsSchema', many=True)

# Schema Instances
owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)

trail_feature_schema = TrailFeatureSchema()
trail_features_schema = TrailFeatureSchema(many=True)

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

trail_points_schema = TrailPointsSchema()

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)
