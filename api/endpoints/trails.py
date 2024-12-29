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
    print("Called Read All function of trail")

    # Query all trails
    trails = Trail.query.all()
    return jsonify(trails_schema.dump(trails))

def read_one(trail_id):
    print("Called Read One function of trail")

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

    # Fetch the route_type 
    route_type = RouteType.query.get(trail.route_id)
    route_type_name = route_type.route_type if route_type else None

    # Fetch the owner 
    owner = Owner.query.get(trail.owner_id)
    owner_name = owner.owner_name if owner else None

    # Prepare the trail points 
    trail_points = [
        {
            "location_point": location_point_schema.dump(
                LocationPoint.query.get(trail_point.location_point_id)
            ) if trail_point.location_point_id else None,
            "sequence_number": trail_point.sequence_number
        }
        for trail_point in trail.trail_points
    ]

    # Return the response with detailed data about the trail
    return jsonify({
        "trail": trail_schema.dump(trail),
        "route_type": route_type_name,
        "owner": owner_name,
        "trail_points": trail_points,
        "features": trail_features
    })

def create():
    print("Called Create function of trail")

    # Authenticate user via the API 
    email = request.headers.get('email')
    password = request.headers.get('password')
    auth_response = authenticate_user(email, password, auth_url)

    # Check if the authentication was successful
    if auth_response["status"] != "success":
        abort(401, "Unauthorized to create trail. Authentication failed.")

    # User authentication is successful; now check if the user is an admin
    user = get_user(request)
    if user is None or not is_admin(user):
        abort(401, "Unauthorized to create trail")

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
        for location_point in trail_points_data:
            location_point['trail_id'] = trail_id
            trail_point = trail_points_schema.load(location_point, session=db.session)
            db.session.add(trail_point)

        # Handle trail features
        for feature in trail_features_data:
            feature['trail_id'] = trail_id
            trail_feature = trail_feature_schema.load(feature, session=db.session)
            db.session.add(trail_feature)

        # Commit the nested relationships of trial points and trail features
        db.session.commit()

        # Query the created trail along with related data
        created_trail = Trail.query.get(trail_id)
        owner = Owner.query.get(created_trail.owner_id)
        route = RouteType.query.get(created_trail.route_id)
        trail_points = TrailPoints.query.filter_by(trail_id=trail_id).all()
        trail_features = TrailFeature.query.filter_by(trail_id=trail_id).all()

        # Construct a detailed response
        response = {
            "trail": trail_schema.dump(created_trail),
            "owner": {
                "owner_id": owner.owner_id,
                "owner_name": owner.owner_name,
                "email": owner.email,
            },
            "route_type": {
                "route_id": route.route_id,
                "route_type": route.route_type,
            },
            "trail_points": [
                {
                    "location_point_id": point.location_point_id,
                    "sequence_number": point.sequence_number,
                } for point in trail_points
            ],
            "trail_features": [
                {
                    "feature_id": feature.feature_id,
                    "feature_name": Feature.query.get(feature.feature_id).feature_name,
                } for feature in trail_features
            ],
        }

        # Return the response
        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        abort(500, f"An error occurred while creating the trail: {str(e)}")

def update(trail_id):
    # Authenticate user
    email = request.headers.get('email')
    password = request.headers.get('password')
    auth_response = authenticate_user(email, password, auth_url)

    if auth_response.get("status") != "success":
        abort(401, "Unauthorized to update trail. Authentication failed.")

    # Fetch the existing trail
    existing_trail = Trail.query.get(trail_id)
    if not existing_trail:
        abort(404, f"Trail with ID {trail_id} not found")

    # Parse input data
    trail_data = request.get_json()

    # Update the fields if present
    if "name" in trail_data:
        existing_trail.name = trail_data["name"]
    if "difficulty" in trail_data:
        existing_trail.difficulty = trail_data["difficulty"]
    if "location" in trail_data:
        existing_trail.location = trail_data["location"]
    if "length" in trail_data:
        existing_trail.length = trail_data["length"]
    if "elevation_gain" in trail_data:
        existing_trail.elevation_gain = trail_data["elevation_gain"]
    if "description" in trail_data:
        existing_trail.description = trail_data["description"]

    # Handle Trail Features
    if "trail_features" in trail_data:
        TrailFeature.query.filter_by(trail_id=trail_id).delete()
        for feature in trail_data["trail_features"]:
            new_feature = TrailFeature(trail_id=trail_id, feature_id=feature["feature_id"])
            db.session.add(new_feature)

    # Handle Trail Points
    if "trail_points" in trail_data:
        TrailPoints.query.filter_by(trail_id=trail_id).delete()
        for point in trail_data["trail_points"]:
            new_point = TrailPoints(
                trail_id=trail_id,
                location_point_id=point["location_point_id"],
                sequence_number=point["sequence_number"]
            )
            db.session.add(new_point)

    # Commit changes
    db.session.commit()

    return jsonify({"message": "Trail updated successfully", "trail": trail_schema.dump(existing_trail)}), 200

def delete(trail_id):
    print("Called Delete function of trail")

    # Authenticate user via the API
    email = request.headers.get('email')
    password = request.headers.get('password')
    auth_response = authenticate_user(email, password, auth_url)

    if auth_response["status"] != "success":
        abort(401, "Unauthorized to delete trail. Authentication failed.")

    # User authentication is successful; now check if the user is an admin or the owner
    user = get_user(request)
    if user is None or (not is_admin(user) and user.owner_id != trail_id):
        abort(401, "Unauthorized to delete trail")

    # Fetch the trail by ID
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

# Authentication
    # Need to check email and password match with API
        # Check it exists in the database
            # Check if the user is an admin

def authenticate_user(email, password, auth_url):
    credentials = {'email': email, 'password': password}
    try:
        response = requests.post(auth_url, json=credentials)
        if response.status_code == 200:
            try:
                json_response = response.json()
                return {"status": "success", "data": json_response}
            except requests.JSONDecodeError:
                return {"status": "error", "message": "Response is not valid JSON.", "response": response.text}
        else:
            return {"status": "error", "message": f"Authentication failed with status code {response.status_code}", "response": response.text}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def get_user(req: Request):
    email = req.headers.get('email')
    user = Owner.query.filter(Owner.email == email).one_or_none()
    return user

def is_admin(user):
    return user.role == "admin" if user else False

