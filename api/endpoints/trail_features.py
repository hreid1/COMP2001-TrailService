from flask import abort, make_response, jsonify, request

from config import db
from models import TrailFeature, Trail, Feature


# Endpoints for the JOIN table between Trail and Feature
# CRUD
    # Create
    # Read
    # Update
    # Delete

# Tables
    # Trail
        # trail_id
        # name
        # difficulty
        # location
        # length
        # elevation_gain
        # description
        # owner_id
        # route_id
    # TrailFeature (JOIN TABLE) Trail -> Feature
        # trail_id
        # feature_id
    # Feature
        # feature_id
        # feature_name

# Sample Data
    # Trail
        # 1, "Plymbridge Circular"
        # 2, "Plymouth Waterfront"
        # 3, "Dartmoor Explorer"
    # Feature
        # 1, "Waterfall"
        # 2, "Scenic View"
        # 3, "Wildlife"
    # Trail Features
        # 1, 1
        # 2, 2
        # 3, 2

def create(trail_id, feature_id):
   
    # Check if the trail and feature exist
    trail = Trail.query.get(trail_id)
    if trail is None:
        abort(404, description=f"Trail with ID {trail_id} not found")

    feature = Feature.query.get(feature_id)
    if feature is None:
        abort(404, description=f"Feature with ID {feature_id} not found")

    # Create a new TrailFeature record
    trail_feature = TrailFeature(trail_id=trail_id, feature_id=feature_id)

    # Add the record to the database
    db.session.add(trail_feature)
    db.session.commit()

    return jsonify(trail_feature), 201

def update(trail_id, feature_id):
    # Check if the trail and feature exist
    trail = Trail.query.get(trail_id)
    if trail is None:
        abort(404, description=f"Trail with ID {trail_id} not found")

    feature = Feature.query.get(feature_id)
    if feature is None:
        abort(404, description=f"Feature with ID {feature_id} not found")

    # Check if the TrailFeature record exists
    trail_feature = TrailFeature.query.filter_by(trail_id=trail_id, feature_id=feature_id).first()
    if trail_feature is None:
        abort(404, description=f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} not found")

    # Update the TrailFeature record
    trail_feature.trail_id = trail_id
    trail_feature.feature_id = feature_id

    # Commit the changes
    db.session.commit()

    return jsonify(trail_feature), 200

def delete(trail_id, feature_id):
    # Check if the TrailFeature record exists
    trail_feature = TrailFeature.query.filter_by(trail_id=trail_id, feature_id=feature_id).first()
    if trail_feature is None:
        abort(404, description=f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} not found")

    # Delete the TrailFeature record
    db.session.delete(trail_feature)
    db.session.commit()

    return make_response(f"TrailFeature with Trail ID {trail_id} and Feature ID {feature_id} has been deleted", 204)
        
