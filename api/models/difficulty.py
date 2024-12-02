from datetime import datetime
import pytz
from database import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import fields

class Difficulty(db.Model):
    __tablename__ = 'difficulty'
    difficultyID = db.Column(db.Integer, primary_key=True)
    difficultyName = db.Column(db.String(255), nullable=False)

    # Relationship with Trail
    #trails = db.relationship('Trail', back_populates='difficulty')

class DifficultySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Difficulty
        load_instance = True
        sqla_session = db.session

    difficultyID = fields.Integer(dump_only=True)
    difficultyName = fields.String(required=True)

difficulty_schema = DifficultySchema()
difficulties_schema = DifficultySchema(many=True)
