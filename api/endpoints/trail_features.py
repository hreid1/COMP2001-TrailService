from flask import abort, make_response, jsonify, request

from config import db
from models import TrailFeature, trail_feature_schema, trail_features_schema


# Endpoints for the JOIN table between Trail and Feature
# CRUD
    # Create
    # Read
    # Update
    # Delete

def read_all():
    trail_features = TrailFeature.query.all()
    return jsonify(trail_features_schema.dump(trail_features))

def read_one(trail_id, feature_id):
    trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if trail_feature:
        return trail_feature_schema.jsonify(trail_feature)
    else:
        abort(404, f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} not found")

def create():
    print("Called Create function of trail_feature")
    trail_feature = request.get_json()
    new_trail_feature = trail_feature_schema.load(trail_feature, session=db.session)
    db.session.add(new_trail_feature)
    db.session.commit()
    return trail_feature_schema.jsonify(new_trail_feature), 201

def update(trail_id, feature_id):
    print("Called Update function of trail_feature")
    trail_feature = request.get_json()
    existing_trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if existing_trail_feature:
        update_trail_feature = trail_feature_schema.load(trail_feature, session=db.session)
        existing_trail_feature.trail_id = update_trail_feature.trail_id
        existing_trail_feature.feature_id = update_trail_feature.feature_id
        db.session.merge(existing_trail_feature)
        db.session.commit()
        return trail_feature_schema.dump(existing_trail_feature), 201
    else:
        abort(404, f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} not found")

def delete(trail_id, feature_id):
    print("Called Delete function of trail_feature")
    existing_trail_feature = TrailFeature.query.get((trail_id, feature_id))
    if existing_trail_feature:
        db.session.delete(existing_trail_feature)
        db.session.commit()
        return make_response(f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} successfully deleted", 204)
    else:
        abort(404, f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} not found")
        
