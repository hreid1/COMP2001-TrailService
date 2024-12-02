-- Insert test data for Owner
INSERT INTO Owner (ownerID, ownerName, email, isAdmin)
VALUES 
(1, 'John Doe', 'john.doe@example.com', TRUE),
(2, 'Jane Smith', 'jane.smith@example.com', FALSE),
(3, 'Mike Johnson', 'mike.johnson@example.com', FALSE);

-- Insert test data for Difficulty
INSERT INTO Difficulty (difficultyID, difficultyName)
VALUES 
(1, 'Easy'),
(2, 'Moderate'),
(3, 'Hard'),
(4, 'Very Hard');

-- Insert test data for RouteType
INSERT INTO RouteType (routeTypeID, routeTypeName)
VALUES 
(1, 'Loop'),
(2, 'Out-and-Back'),
(3, 'Point-to-Point');

-- Insert test data for Location
INSERT INTO Location (locationID, locationName)
VALUES 
(1, 'Yosemite National Park'),
(2, 'Rocky Mountain National Park'),
(3, 'Grand Canyon National Park'),
(4, 'Zion National Park');

-- Insert test data for Trail
INSERT INTO Trail (trailID, trailName, rating, difficultyID, routeTypeID, locationID, trailDescription, trailDistance, trailElevationGain, averageTimeToComplete, ownerID)
VALUES 
(1, 'Yosemite Valley Loop', 4.5, 1, 1, 1, 'A scenic loop around the valley with beautiful views of Yosemite Falls and Half Dome.', 12.5, 500, 3.5, 1),
(2, 'Rocky Mountain Summit', 3.9, 2, 2, 2, 'A challenging out-and-back trail leading to the summit of a mountain with panoramic views.', 16.8, 1200, 6.0, 2),
(3, 'Grand Canyon Rim Trail', 4.8, 1, 3, 3, 'A point-to-point trail along the rim of the Grand Canyon, offering stunning views of the canyon below.', 18.2, 600, 5.0, 3),
(4, 'Angels Landing', 4.9, 3, 2, 4, 'A very hard out-and-back trail leading to a summit with breathtaking views of Zion Canyon.', 5.4, 4500, 4.5, 2);

-- Insert test data for TrailFeature
INSERT INTO TrailFeature (featureID, featureName)
VALUES 
(1, 'Waterfall'),
(2, 'Panoramic View'),
(3, 'Rock Scramble'),
(4, 'Wildlife Viewing');

-- Insert test data for TrailFeatureJoin
INSERT INTO TrailFeatureJoin (trailID, featureID)
VALUES 
(1, 2), -- Yosemite Valley Loop - Panoramic View
(1, 1), -- Yosemite Valley Loop - Waterfall
(2, 2), -- Rocky Mountain Summit - Panoramic View
(3, 2), -- Grand Canyon Rim Trail - Panoramic View
(4, 3), -- Angels Landing - Rock Scramble
(4, 2); -- Angels Landing - Panoramic View

-- Insert test data for LocationPoint
INSERT INTO LocationPoint (locationPointID, trailID, latitude, longitude, sequenceNumber)
VALUES 
(1, 1, 37.7749, -122.4194, 1), -- Start of Yosemite Valley Loop
(2, 1, 37.7560, -122.4060, 2), -- Midway point of Yosemite Valley Loop
(3, 2, 39.7456, -105.5083, 1), -- Start of Rocky Mountain Summit
(4, 2, 39.7345, -105.5292, 2), -- Midway point of Rocky Mountain Summit
(5, 3, 36.1069, -112.1129, 1), -- Start of Grand Canyon Rim Trail
(6, 3, 36.0602, -112.1141, 2), -- Midway point of Grand Canyon Rim Trail
(7, 4, 37.2560, -113.1374, 1), -- Start of Angels Landing
(8, 4, 37.2619, -113.1458, 2); -- Midway point of Angels Landing
