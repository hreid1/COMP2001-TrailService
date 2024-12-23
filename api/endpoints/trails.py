from flask import abort, make_response, jsonify, request

from config import db
from models import Trail, trail_schema, trails_schema, location_point_schema, LocationPoint, Feature, TrailFeature, TrailPoints


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

    # Relationships
    # trail_points = db.relationship(TrailPoints, backref='trails_trail_points', single_parent=True)

# CRUD functions
    # Create
    # Read
        # Read one
            # Need to return associated RouteType, Owner
                # Via JOIN TABLES
            # Tables
                # Owner (owners)
                    # owner_id
                    # owner_name
                    # email
                    # role
                # RouteType (route_type)
                    # route_type_id
                    # route_type
                # TrailPoints (trail_points) JOIN TABLE
                    # trail_id
                    # location_point_id
                    # sequence_number
                # LocationPoint (location_point)
                    # location_point_id
                    # longitude
                    # latitude
                    # description
        # Read all
    # Update
    # Delete
        # Can only delete trail if admin/author of trail
# Need to check user is admin before anything
    # via auth.py
        # Check if user is admin
        # Check if user exists
        # Check if user is authenticated
        # Check if user is authorised to perform action

def read_all():
    # Query all trails
    trails = Trail.query.all()
    return jsonify(trails_schema.dump(trails))

def read_one(trail_id):
    # Query the trail by ID
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    # Fetch associated features using the TrailFeature relationship
    trail_features = [
        {
            "feature_id": trail_feature.feature_id,
            "feature_name": Feature.query.get(trail_feature.feature_id).feature_name
        }
        for trail_feature in trail.trail_features
    ]
    
    return jsonify({
        "trail": trail_schema.dump(trail),
        "route_type": trail.route_type.route_type,
        "owner": trail.owners.owner_name,
        "trail_points": [
            {
                "location_point": location_point_schema.dump(
                    LocationPoint.query.get(trail_point.location_point_id)
                ),
                "sequence_number": trail_point.sequence_number
            }
            for trail_point in trail.trail_points
        ],
        "features": trail_features
    })



def create():
    print("Called Create function of trail")

    # Parse the incoming JSON data
    trail_data = request.get_json()

    # Validate that required fields are provided
    required_fields = ["name", "difficulty", "location", "length", "elevation_gain", "description", "owner_id", "route_id"]
    for field in required_fields:
        if field not in trail_data:
            abort(400, f"Missing required field: {field}")

    try:
        # Create the new trail object from the provided data
        new_trail = trail_schema.load(trail_data, session=db.session)

        # Add the trail to the session and commit to save it
        db.session.add(new_trail)
        db.session.commit()  # This will save the trail and assign a trail_id

        # Now that the trail is saved, we can retrieve the trail_id
        trail_id = new_trail.trail_id

        # Return the newly created trail's data (without points or features)
        return trail_schema.jsonify(new_trail), 201

    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        print(f"Error occurred during trail creation: {e}")
        abort(500, "An error occurred while creating the trail")

        # Need to add TrailPoints and TrailFeatures
            # Modify Swagger to implement




def update(trail_id):
    print("Called Update function of trail")
    trail_data = request.get_json()
 
    # Fetch the existing trail
    existing_trail = Trail.query.get(trail_id)
    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Update the trail fields
    updated_trail = trail_schema.load(trail_data, session=db.session, partial=True)
    existing_trail.name = updated_trail.name
    existing_trail.difficulty = updated_trail.difficulty
    existing_trail.location = updated_trail.location
    existing_trail.length = updated_trail.length
    existing_trail.elevation_gain = updated_trail.elevation_gain
    existing_trail.description = updated_trail.description
    existing_trail.owner_id = updated_trail.owner_id
    existing_trail.route_id = updated_trail.route_id

    # Update TrailPoints if provided
    if "trail_points" in trail_data:
        # Delete existing trail points for this trail
        TrailPoints.query.filter_by(trail_id=trail_id).delete()
        # Add new trail points
        for point in trail_data["trail_points"]:
            new_point = TrailPoints(
                trail_id=trail_id,
                location_point_id=point["location_point_id"],
                sequence_number=point["sequence_number"]
            )
            db.session.add(new_point)

    # Update TrailFeatures if provided
    if "features" in trail_data:
        # Delete existing trail features for this trail
        TrailFeature.query.filter_by(trail_id=trail_id).delete()
        # Add new trail features
        for feature in trail_data["features"]:
            new_feature = TrailFeature(
                trail_id=trail_id,
                feature_id=feature["feature_id"]
            )
            db.session.add(new_feature)

    # Commit all changes
    db.session.commit()

    # Return the updated trail details
    return jsonify({
        "trail": trail_schema.dump(existing_trail),
        "trail_points": [
            {
                "location_point_id": point.location_point_id,
                "sequence_number": point.sequence_number
            } for point in existing_trail.trail_points
        ],
        "features": [
            {
                "feature_id": feature.feature_id,
                "feature_name": Feature.query.get(feature.feature_id).feature_name
            } for feature in TrailFeature.query.filter_by(trail_id=trail_id).all()
        ]
    }), 200


def delete(trail_id):
    print("Called Delete function of trail")

    # Fetch the trail
    existing_trail = Trail.query.get(trail_id)
    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Delete associated TrailPoints and TrailFeatures
    TrailPoints.query.filter_by(trail_id=trail_id).delete()
    TrailFeature.query.filter_by(trail_id=trail_id).delete()

    # Delete the trail itself
    db.session.delete(existing_trail)
    db.session.commit()

    return make_response(f"Trail with ID {trail_id} successfully deleted", 204)
