# models.py
from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

class Owner(db.Model): 
    __tablename__ = 'owners'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship
    trails = db.relationship(
        'Trail',
        back_populates='owner',
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Trail.trail_id"
    )

class RouteType(db.Model):
    __tablename__ = 'route_types'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_type = db.Column(db.String(50), nullable=False)

    # Relationship
    trails = db.relationship('Trail', back_populates='route_type')

class Trail(db.Model):
    __tablename__ = 'trails'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('CW2.owners.owner_id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('CW2.route_types.route_id'), nullable=False)

    # Relationships
    owner = db.relationship('Owner', back_populates='trails')
    route_type = db.relationship('RouteType', back_populates='trails')
    trail_features = db.relationship('TrailFeature', back_populates='trail', cascade="all, delete, delete-orphan")
    location_points = db.relationship('LocationPoint', back_populates='trail', cascade="all, delete, delete-orphan")

class TrailFeature(db.Model):
    __tablename__ = 'trail_features'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('CW2.features.feature_id'), primary_key=True)

    # Relationships
    trail = db.relationship('Trail', back_populates='trail_features')
    feature = db.relationship('Feature', back_populates='trail_features')

class Feature(db.Model):
    __tablename__ = 'features'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    feature_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feature_name = db.Column(db.String(50), nullable=False)

    # Relationships
    trail_features = db.relationship('TrailFeature', back_populates='feature')

class LocationPoint(db.Model):
    __tablename__ = 'location_points'
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    # Entity columns
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)

    # Relationships
    trail = db.relationship('Trail', back_populates='location_points')

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    trails = fields.Nested('TrailSchema', many=True)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True

class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

    trails = fields.Nested('TrailSchema', many=True)

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session

    trail_features = fields.Nested('TrailFeatureSchema', many=True)

class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

    trail = fields.Nested('TrailSchema')

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

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)