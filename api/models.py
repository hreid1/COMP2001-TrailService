# models.py
from config import db, ma

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

    # Relationship
    owner = db.relationship('Owner', back_populates='trails')

class OwnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Owner
        sqla_session = db.session
        load_instance = True
        include_fk = True

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        sqla_session = db.session
        load_instance = True
        include_fk = True

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)