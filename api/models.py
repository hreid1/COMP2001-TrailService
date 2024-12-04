# models.py
from config import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

# Models
    # Owner (One-to-many) -> Trail
    # RouteType (One-to-many) -> Trail
    # Trail-Feature (JOIN TABLE) -> Trail, Feature
    # Feature (One-to-many) -> Trail-Feature -> (One-to-many) Trail
    # LocationPoint (One-to-many) -> Trail
    # Trail 
# Schemas
    # OwnerSchema 
    # RouteTypeSchema
    # TrailSchema
    # FeatureSchema
    # LocationPointSchema
    # TrailFeatureSchema (JOIN TABLE)

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

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)