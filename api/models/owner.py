from database import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

class Owner(db.Model):
    __tablename__ = 'owner'
    ownerID = db.Column(db.Integer, primary_key=True)
    ownerName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    # Relationship with Trail
    #trails = db.relationship('Trail', back_populates='owner')

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session

    ownerID = fields.Integer(dump_only=True)
    ownerName = fields.String(required=True)
    email = fields.String(required=True)
    isAdmin = fields.Boolean(required=True)

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)
