from flask import abort, make_response, jsonify, request
from config import db
from models import Feature, feature_schema, features_schema

# Endpoint for the features of the trail
    # CRUD
        # Create
        # Read
            # Read one
            # Read all
        # Update
        # Delete

def read_one(feature_id):
    feature = Feature.query.get(feature_id)
    if feature is not None:
        return feature_schema.jsonify(feature)
    else:
        abort(404, f"Feature with ID {feature_id} not found")

def read_all():
    features = Feature.query.all()
    return features_schema.jsonify(features)

def create(feature):
    new_feature = feature_schema.load(feature, session=db.session)
    db.session.add(new_feature)
    db.session.commit()
    return feature_schema.jsonify(new_feature), 201

def update(feature_id, feature):
    existing_feature = Feature.query.get(feature_id)
    if existing_feature:
        update_feature = feature_schema.load(feature, session=db.session)
        existing_feature.feature = update_feature.feature
        db.session.merge(existing_feature)
        db.session.commit()
        return feature_schema.dump(existing_feature), 201
    else:
        abort(404, f"Feature with ID {feature_id} not found")

def delete(feature_id):
    existing_feature = Feature.query.get(feature_id)
    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return make_response(f"Feature with ID {feature_id} successfully deleted", 204)
    else:
        abort(404, f"Feature with ID {feature_id} not found")
        