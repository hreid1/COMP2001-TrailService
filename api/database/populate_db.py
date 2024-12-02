from datetime import datetime
from config import app, db
from models import Owner, Difficulty, RouteType, Location, Trail, TrailFeature, LocationPoint, TrailFeatureJoin

# Sample data
DATA = {
    "owners": [
        {"ownerID": 1, "ownerName": "John Doe", "email": "john.doe@example.com", "isAdmin": True},
        {"ownerID": 2, "ownerName": "Jane Smith", "email": "jane.smith@example.com", "isAdmin": False},
        {"ownerID": 3, "ownerName": "Mike Johnson", "email": "mike.johnson@example.com", "isAdmin": False},
    ],
    "difficulties": [
        {"difficultyID": 1, "difficultyName": "Easy"},
        {"difficultyID": 2, "difficultyName": "Moderate"},
        {"difficultyID": 3, "difficultyName": "Hard"},
    ],
    "route_types": [
        {"routeTypeID": 1, "routeTypeName": "Loop"},
        {"routeTypeID": 2, "routeTypeName": "Out and Back"},
        {"routeTypeID": 3, "routeTypeName": "Point to Point"},
    ],
    "locations": [
        {"locationID": 1, "locationName": "Location A", "timestamp": "2024-11-26 09:10:24"},
        {"locationID": 2, "locationName": "Location B", "timestamp": "2024-11-26 11:17:54"},
        {"locationID": 3, "locationName": "Location C", "timestamp": "2024-11-26 12:15:03"},
    ],
    "trails": [
        {"id": 1, "trailName": "Trail 1", "rating": 4.5, "trailDescription": "Beautiful trail", "trailDistance": 10.5, "trailElevationGain": 500, "averageTimeToComplete": 3.5, "difficultyID": 1, "routeTypeID": 1, "locationID": 1, "ownerID": 1},
        {"id": 2, "trailName": "Trail 2", "rating": 3.8, "trailDescription": "Challenging trail", "trailDistance": 8.2, "trailElevationGain": 300, "averageTimeToComplete": 2.8, "difficultyID": 2, "routeTypeID": 2, "locationID": 2, "ownerID": 2},
        {"id": 3, "trailName": "Trail 3", "rating": 4.2, "trailDescription": "Scenic trail", "trailDistance": 12.0, "trailElevationGain": 600, "averageTimeToComplete": 4.0, "difficultyID": 3, "routeTypeID": 3, "locationID": 3, "ownerID": 3},
    ],
    "trail_features": [
        {"featureID": 1, "featureName": "Waterfall"},
        {"featureID": 2, "featureName": "Cave"},
        {"featureID": 3, "featureName": "Scenic View"},
    ],
    "location_points": [
        {"pointID": 1, "locationID": 1, "latitude": 34.052235, "longitude": -118.243683},
        {"pointID": 2, "locationID": 2, "latitude": 36.169941, "longitude": -115.139832},
        {"pointID": 3, "locationID": 3, "latitude": 40.712776, "longitude": -74.005974},
    ],
    "trail_feature_joins": [
        {"id": 1, "trailID": 1, "featureID": 1},
        {"id": 2, "trailID": 2, "featureID": 2},
        {"id": 3, "trailID": 3, "featureID": 3},
    ],
}

with app.app_context():
    db.drop_all()
    db.create_all()

    for owner_data in DATA["owners"]:
        new_owner = Owner(**owner_data)
        db.session.add(new_owner)

    for difficulty_data in DATA["difficulties"]:
        new_difficulty = Difficulty(**difficulty_data)
        db.session.add(new_difficulty)

    for route_type_data in DATA["route_types"]:
        new_route_type = RouteType(**route_type_data)
        db.session.add(new_route_type)

    for location_data in DATA["locations"]:
        location_data["timestamp"] = datetime.strptime(location_data["timestamp"], "%Y-%m-%d %H:%M:%S")
        new_location = Location(**location_data)
        db.session.add(new_location)

    for trail_data in DATA["trails"]:
        new_trail = Trail(**trail_data)
        db.session.add(new_trail)

    for trail_feature_data in DATA["trail_features"]:
        new_trail_feature = TrailFeature(**trail_feature_data)
        db.session.add(new_trail_feature)

    for location_point_data in DATA["location_points"]:
        new_location_point = LocationPoint(**location_point_data)
        db.session.add(new_location_point)

    for trail_feature_join_data in DATA["trail_feature_joins"]:
        new_trail_feature_join = TrailFeatureJoin(**trail_feature_join_data)
        db.session.add(new_trail_feature_join)

    db.session.commit()
    print("Tables created and data inserted successfully.")