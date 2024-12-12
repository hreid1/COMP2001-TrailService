from flask import abort, make_response, jsonify, request
from config import db
from models import TrailFeature, trail_feature_schema, trail_features_schema

# CRUD Operations for Trail Features
    # Create
    # Read
        # Read one
        # Read all
    # Update
    # Delete

# Read all TrailFeature records
def read_all():
    trail_features = TrailFeature.query.all()
    return jsonify(trail_features_schema.dump(trail_features)), 200

# Read one TrailFeature by composite key (trail_id and feature_id)
def read_one(trail_id, feature_id):
    trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if trail_feature:
        return trail_feature_schema.jsonify(trail_feature), 200
    else:
        abort(404, f"Trail Feature with trail_id {trail_id} and feature_id {feature_id} not found")

# Create a new TrailFeature
def create(trail_feature_data):
    new_trail_feature = trail_feature_schema.load(trail_feature_data, session=db.session)
    db.session.add(new_trail_feature)
    db.session.commit()
    return trail_feature_schema.jsonify(new_trail_feature), 201

# Update an existing TrailFeature
def update(trail_id, feature_id, trail_feature_data):
    existing_trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if existing_trail_feature:
        update_data = trail_feature_schema.load(trail_feature_data, session=db.session)
        existing_trail_feature.trail_id = update_data.trail_id
        existing_trail_feature.feature_id = update_data.feature_id
        db.session.commit()
        return trail_feature_schema.jsonify(existing_trail_feature), 200
    else:
        abort(404, f"Trail Feature with trail_id {trail_id} and feature_id {feature_id} not found")

# Delete a TrailFeature
def delete(trail_id, feature_id):
    existing_trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if existing_trail_feature:
        db.session.delete(existing_trail_feature)
        db.session.commit()
        return make_response(f"Trail Feature with trail_id {trail_id} and feature_id {feature_id} successfully deleted", 204)
    else:
        abort(404, f"Trail Feature with trail_id {trail_id} and feature_id {feature_id} not found")
