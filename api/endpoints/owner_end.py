from flask import abort, make_response
from api.database.config import db
from models import Owner, owner_schema, owners_schema

def read_all():
    owners = Owner.query.order_by(Owner.ownerName).all()
    owners = owners_schema.dump(owners)
    return owners

def read_one(owner_id):
    owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if owner is not None:
        owner = owner_schema.dump(owner)
    else:
        abort(404, f'Owner not found for Id: {owner_id}')
    return owner

def create(owner):
    ownerName = owner.get('ownerName')
    existing_owner = Owner.query.filter(Owner.ownerName == ownerName).one_or_none()
    if existing_owner is None:
        new_owner = Owner(ownerName=ownerName)
        db.session.add(new_owner)
        db.session.commit()
        return owner_schema.dump(new_owner), 201
    else:
        abort(409, f'Owner {ownerName} exists already')

def update(owner_id, owner):
    update_owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if update_owner is not None:
        owner_schema.load(owner, session=db.session)
        db.session.commit()
        return owner_schema.dump(update_owner), 200
    else:
        abort(404, f'Owner not found for Id: {owner_id}')

def delete(owner_id):
    owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if owner is not None:
        db.session.delete(owner)
        db.session.commit()
        return make_response(f'Owner {owner_id} deleted', 204)
    else:
        abort(404, f'Owner not found for Id: {owner_id}')
        