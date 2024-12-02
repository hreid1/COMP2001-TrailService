from flask import abort, make_response
from api.database.config import db
from models import TrailFeature, trail_feature_schema, trail_features_schema

# Get all trail features
def read_all():
    features = TrailFeature.query.order_by(TrailFeature.featureName).all()
    return trail_features_schema.dump(features)

# Get one trail feature by ID
def read_one(feature_id):
    feature = TrailFeature.query.filter(TrailFeature.featureID == feature_id).one_or_none()
    if feature:
        return trail_feature_schema.dump(feature)
    else:
        abort(404, f'TrailFeature not found for Id: {feature_id}')

# Create a new trail feature
def create(feature):
    featureName = feature.get('featureName')
    existing_feature = TrailFeature.query.filter(TrailFeature.featureName == featureName).one_or_none()
    
    if existing_feature is None:
        new_feature = TrailFeature(featureName=featureName)
        db.session.add(new_feature)
        db.session.commit()
        return trail_feature_schema.dump(new_feature), 201  # Created response
    else:
        abort(409, f'TrailFeature {featureName} already exists')

# Update an existing trail feature
def update(feature_id, feature):
    update_feature = TrailFeature.query.filter(TrailFeature.featureID == feature_id).one_or_none()
    
    if update_feature:
        update_feature.featureName = feature.get('featureName', update_feature.featureName)
        db.session.commit()
        return trail_feature_schema.dump(update_feature), 200  # OK response
    else:
        abort(404, f'TrailFeature not found for Id: {feature_id}')

# Delete a trail feature
def delete(feature_id):
    feature = TrailFeature.query.filter(TrailFeature.featureID == feature_id).one_or_none()
    
    if feature:
        db.session.delete(feature)
        db.session.commit()
        return make_response(f'TrailFeature {feature_id} deleted', 204)  # No content response
    else:
        abort(404, f'TrailFeature not found for Id: {feature_id}')
