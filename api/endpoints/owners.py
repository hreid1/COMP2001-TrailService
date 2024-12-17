from flask import abort, make_response, jsonify, request
from config import db, ma
from models import Owner, owner_schema, owners_schema

# CRUD Operations
    # Create
    # Read
        # Read one
        # Read all
    # Update
    # Delete

def read_one(owner_id):
    owner = Owner.query.get(owner_id)
    if owner is not None:
        return owner_schema.jsonify(owner)
    else:
        abort(404, f"Owner with ID {owner_id} not found")

def read_all():
    owners = Owner.query.all()
    return owners_schema.jsonify(owners)

def create(owner):
    print("Called Create function of owner")
    new_owner = owner_schema.load(owner, session=db.session)
    db.session.add(new_owner)
    db.session.commit()
    return owner_schema.jsonify(new_owner), 201

def update(owner_id, owner):
    print("Called Update function of owner")
    existing_owner = Owner.query.get(owner_id)
    if existing_owner:
        update_owner = owner_schema.load(owner, session=db.session)
        existing_owner.name = update_owner.name
        existing_owner.email = update_owner.email
        db.session.merge(existing_owner)
        db.session.commit()
        return owner_schema.dump(existing_owner), 201
    else:
        abort(404, f"Owner with ID {owner_id} not found")

def delete(owner_id):
    print("Called Delete function of owner")
    existing_owner = Owner.query.get(owner_id)
    if existing_owner:
        db.session.delete(existing_owner)
        db.session.commit()
        return make_response(f"Owner with ID {owner_id} successfully deleted", 204)
    else:
        abort(404, f"Owner with ID {owner_id} not found")

