from flask import abort, make_response
from api.database.config import db
from models import Owner, owner_schema, owners_schema

# Get all owners
def read_all():
    owners = Owner.query.order_by(Owner.ownerName).all()
    owners = owners_schema.dump(owners)
    return owners

# Get one owner by ID
def read_one(owner_id):
    owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if owner:
        owner = owner_schema.dump(owner)
    else:
        abort(404, f'Owner not found for Id: {owner_id}')
    return owner

# Create a new owner
def create(owner):
    ownerName = owner.get('ownerName')
    if not ownerName:
        abort(400, description="Owner name is required")
    
    existing_owner = Owner.query.filter(Owner.ownerName == ownerName).one_or_none()
    if existing_owner is None:
        new_owner = Owner(ownerName=ownerName)
        db.session.add(new_owner)
        db.session.commit()
        return owner_schema.dump(new_owner), 201  # Created response
    else:
        abort(409, f'Owner {ownerName} exists already')

# Update an existing owner
def update(owner_id, owner):
    update_owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if update_owner:
        update_owner.ownerName = owner.get('ownerName', update_owner.ownerName)
        # If other fields need to be updated, you can add them here
        db.session.commit()
        return owner_schema.dump(update_owner), 200  # OK response
    else:
        abort(404, f'Owner not found for Id: {owner_id}')

# Delete an owner
def delete(owner_id):
    owner = Owner.query.filter(Owner.ownerID == owner_id).one_or_none()
    if owner:
        db.session.delete(owner)
        db.session.commit()
        return make_response(f'Owner {owner_id} deleted', 204)  # No content response
    else:
        abort(404, f'Owner not found for Id: {owner_id}')
