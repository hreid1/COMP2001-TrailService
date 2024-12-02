from datetime import datetime
import pytz
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func

from api.database.config import db, ma

class Difficulty(db.Model):
    __tablename__ = 'difficulty'
    difficultyID = db.Column(db.Integer, primary_key=True)
    difficultyName = db.Column(db.String(255), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

class DifficultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Difficulty
        load_instance = True
        sqla_session = db.session

    difficultyID = fields.Integer(dump_only=True)
    difficultyName = fields.String(required=True)
    timestamp = fields.DateTime()

difficulty_schema = DifficultySchema()
difficulties_schema = DifficultySchema(many=True)

