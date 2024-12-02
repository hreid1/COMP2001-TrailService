from flask import abort, make_response
from api.database.config import db
from models import TrailFeatureJoin, trail_feature_join_schema

# Associate a trail with a feature (creating a TrailFeatureJoin)
def create_join(trail_id, feature_id):
    # Check if the join already exists
    existing_join = TrailFeatureJoin.query.filter(TrailFeatureJoin.trailID == trail_id, 
                                                  TrailFeatureJoin.featureID == feature_id).one_or_none()
    if existing_join is None:
        new_join = TrailFeatureJoin(trailID=trail_id, featureID=feature_id)
        db.session.add(new_join)
        db.session.commit()
        return trail_feature_join_schema.dump(new_join), 201  # Created response
    else:
        abort(409, f'Trail {trail_id} already has Feature {feature_id} associated')

# Remove a trail feature association (delete a TrailFeatureJoin)
def delete_join(trail_id, feature_id):
    join = TrailFeatureJoin.query.filter(TrailFeatureJoin.trailID == trail_id, 
                                         TrailFeatureJoin.featureID == feature_id).one_or_none()
    
    if join:
        db.session.delete(join)
        db.session.commit()
        return make_response(f'Trail {trail_id} and Feature {feature_id} association deleted', 204)
    else:
        abort(404, f'Association not found between Trail {trail_id} and Feature {feature_id}')
