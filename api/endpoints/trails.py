from flask import abort, make_response, jsonify, request, Request
import requests
from config import db
from models import Trail, trail_schema, trails_schema, location_point_schema, LocationPoint, Feature, TrailFeature, TrailPoints, Feature, RouteType, Owner, trail_points_schema, trail_feature_schema

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
            # Need to return associated RouteType, Owner, Feature
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
                # TrailFeature (trail_features) JOIN TABLE
                    # trail_id
                    # feature_id
                # Feature (features)
                    # feature_id
                    # feature_name
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

# Authentication -> Basic Auth + Swagger
    # Rules
        # Admins can perform all CRUD actions
        # Users can only read trails
    # Steps
        # Check auth

    # Sample Data
            # Databse Data
            # owner_name: "Grace Hopper", email: "grace@plymouth.ac.uk", role: "admin"
            # owner_name: "Tim Berners-Lee", email: "tim@plymouth.ac.uk, role; "user"

        # API Data -> No role assigned
        # URL -> https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users
            # username: "Grace Hopper", email: "grace@plymouth.ac.uk", password: "ISAD123!"
            # username: "Tim Berners-Lee", email: "tim@plymouth.ac.uk", password: "COMP2001!"
            # username: "Ada Lovelace", email: "ada@plymouth.ac.uk", password: "insecurePassword"

                # API integration basically to assess that the user is real

                # auth.py -> authenticate_user(email, password)
                    # Matches email and password to the API

auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

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

    # Extract nested trail points and features
    trail_points_data = trail_data.pop('trail_points', [])
    trail_features_data = trail_data.pop('trail_features', [])

    try:
        # Create the new trail object from the provided data
        new_trail = trail_schema.load(trail_data, session=db.session)

        # Add the trail to the session and commit to save it
        db.session.add(new_trail)
        db.session.commit()

        # Retrieve the newly created trail_id
        trail_id = new_trail.trail_id

        # Handle trail points
        for point in trail_points_data:
            point['trail_id'] = trail_id
            trail_point = trail_points_schema.load(point, session=db.session)
            db.session.add(trail_point)

        # Handle trail features
        for feature in trail_features_data:
            feature['trail_id'] = trail_id
            trail_feature = trail_feature_schema.load(feature, session=db.session)
            db.session.add(trail_feature)

        # Commit the nested relationships
        db.session.commit()

        # Return the newly created trail's data
        return trail_schema.jsonify(new_trail), 201

    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        print(f"Error occurred during trail creation: {e}")
        abort(500, "An error occurred while creating the trail")

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

    user = check_owner_or_admin(trail_id)

    # Step 2: Fetch the trail by ID
    existing_trail = Trail.query.get(trail_id)
    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Step 3: Delete associated TrailPoints and TrailFeatures
    TrailPoints.query.filter_by(trail_id=trail_id).delete()
    TrailFeature.query.filter_by(trail_id=trail_id).delete()

    # Step 4: Delete the trail itself
    db.session.delete(existing_trail)
    db.session.commit()

    # Step 5: Return a success message
    return make_response(f"Trail with ID {trail_id} successfully deleted", 204)

def check_auth():
    if not user_exists(request):
        abort(401, "Invalid credentials")
        
    user = get_user(request)
    if user is None:
        abort(401, "User not found in database")
        
    return user

def check_admin():
    user = check_auth()
    if not is_admin(user):
        abort(403, "Admin access required")
    return user

def check_owner_or_admin(trail_id):
    user = check_auth()
    
    trail = Trail.query.get(trail_id)
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")
        
    if not is_admin(user) and trail.owner_id != user.owner_id:
        abort(403, "Not authorized to modify this trail")
        
    return user

def user_exists(req: Request) -> bool:
    email = req.headers.get("email")
    password = req.headers.get("password")

    if not email or not password:
        return False
    
    try:
        response = requests.post(
            auth_url, 
            json={"email": email, "password": password},
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_user(req: Request) -> Owner:
    email = req.headers.get("email")
    return Owner.query.filter(Owner.email == email).one_or_none()

def is_admin(user: Owner) -> bool:
    return user and user.role == "admin"