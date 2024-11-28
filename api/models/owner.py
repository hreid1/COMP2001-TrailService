from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

from config import db, ma

class Owner(db.Model):
    __tablename__ = 'owner'
    ownerID = db.Column(db.Integer, primary_key=True)
    ownerName = db.Column(db.String(255), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        load_instance = True
        sqla_session = db.session

    ownerID = fields.Integer(dump_only=True)
    ownerName = fields.String(required=True)
    timestamp = fields.DateTime()

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)