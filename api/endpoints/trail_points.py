

# CRUD operations for TrailPoints (JOIN TABLE) Trail -> LocationPoint

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
    # TrailPoints (JOIN TABLE) Trail -> LocationPoint
        # trail_id -> Trail.trail_id
        # location_point_id -> LocationPoint.location_point_id
        # sequenceNumber
    # LocationPoint
        # location_point_id
        # longitude
        # latitude
        # description

# Sample Data
    # Trail
        # 1, "Plymbridge Circular"
        # 2, "Plymouth Waterfront"
        # 3, "Dartmoor Explorer"
    # LocationPoint
        # Point A: -123.3656, 48.4284
        # Point B: -123.3657, 48.4285
        # Point C: -123.3658, 48.4286
        # Point D: -123.3659, 48.4287
        # Point E: -123.3660, 48.4288
        # Point F: -123.3661, 48.4289
        # Point G: -123.3662, 48.4290
        # Point H: -123.3663, 48.4291
    # Trail Points
        # Plymbridge Circular
            # Point A, 1
            # Point B, 2
            # Point C, 3
            # Point D, 4
            # ...
        # Plymouth Waterfront
            # Point F, 1
            # Point G, 2
            # Point H, 3
        # Dartmoor Explorer
            # Point A, 1
            # Point B, 2
            # Point C, 3





