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

# Trail Model

class Trail(db.Model):
    __tablename__ = "trails"
    __table__args__ = {"schema": "CW2", "extend_existing": True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    length = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("CW2.owners.owner_id"), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey("CW2.routetype.route_id"), nullable=False)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    owner_id = fields.Integer(required=True)

# RouteType Model
class RouteType(db.Model):
    __tablename__ = "routetype"
    __table__args__ = {"schema": "CW2", "extend_existing": True}

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_type = db.Column(db.String(50), nullable=False)

class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session

class Owner(db.Model):
    __tablename__ = "owners"
    __table__args__ = {"schema": "CW2", "extend_existing": True}

    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Boolean, nullable=False)

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)

route_schema = RouteTypeSchema()
routes_schema = RouteTypeSchema(many=True)

