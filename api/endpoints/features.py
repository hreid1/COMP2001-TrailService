from flask import abort, make_response, jsonify, request

from config import db
from models import Feature, features_schema, feature_schema

# Endpoints for features
# CRUD
    # Create
    # Read
    # Update
    # Delete

def read_all():
    features = Feature.query.all()
    return jsonify(features_schema.dump(features))  # No change needed for this

def read_one(feature_id):
    feature = Feature.query.get(feature_id)
    if feature:
        return features_schema.dump(feature)  # Use dump here for single object
    else:
        abort(404, f"Feature with ID {feature_id} not found")

def create():
    print("Called Create function of feature")
    feature = request.get_json()
    new_feature = features_schema.load(feature, session=db.session)
    db.session.add(new_feature)
    db.session.commit()
    return features_schema.jsonify(new_feature), 201

def update(feature_id):
    print("Called Update function of feature")
    feature = request.get_json()
    existing_feature = Feature.query.get(feature_id)
    if existing_feature:
        update_feature = features_schema.load(feature, session=db.session)
        existing_feature.feature_name = update_feature.feature_name
        db.session.merge(existing_feature)
        db.session.commit()
        return features_schema.dump(existing_feature), 201
    else:
        abort(404, f"Feature with ID {feature_id} not found")

def delete(feature_id):
    print("Called Delete function of feature")
    existing_feature = Feature.query.get(feature_id)
    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return features_schema.dump(existing_feature), 201
    else:
        abort(404, f"Feature with ID {feature_id} not found")
