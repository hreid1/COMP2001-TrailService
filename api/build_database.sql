-- Drop the Trail_Feature join table first
DROP TABLE IF EXISTS Trail_Feature;

-- Drop the TrailPoints table
DROP TABLE IF EXISTS TrailPoints;

-- Drop the LocationPoint table
DROP TABLE IF EXISTS LocationPoint;

-- Drop the Feature table
DROP TABLE IF EXISTS Feature;

-- Drop the Trail table
DROP TABLE IF EXISTS Trail;

-- Drop the RouteType table
DROP TABLE IF EXISTS RouteType;

-- Drop the Owner table
DROP TABLE IF EXISTS [Owner];


GO
CREATE SCHEMA CW2;
GO

-- Create the Owner table with BIT for boolean fields under CW2 schema
CREATE TABLE CW2.Owner (
    owner_id INT PRIMARY KEY,
    owner_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_admin BIT NOT NULL  
);

-- Create the RouteType table under CW2 schema
CREATE TABLE CW2.RouteType (
    route_id INT PRIMARY KEY,
    route_type VARCHAR(50) NOT NULL
);

-- Create the Trail table with foreign keys to Owner and RouteType under CW2 schema
CREATE TABLE CW2.Trail (
    trail_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    length DECIMAL(6,2) NOT NULL,
    elevation_gain DECIMAL(6,2) NOT NULL,
    description TEXT,
    owner_id INT,
    route_id INT,
    FOREIGN KEY (owner_id) REFERENCES CW2.Owner(owner_id),
    FOREIGN KEY (route_id) REFERENCES CW2.RouteType(route_id)
);

-- Create the Feature table under CW2 schema
CREATE TABLE CW2.Feature (
    trail_feature_id INT PRIMARY KEY,
    trail_feature VARCHAR(255) NOT NULL
);

-- Create the Trail-Feature join table linking Trail and Feature under CW2 schema
CREATE TABLE CW2.Trail_Feature (
    trail_id INT,
    trail_feature_id INT,
    PRIMARY KEY (trail_id, trail_feature_id),
    FOREIGN KEY (trail_id) REFERENCES CW2.Trail(trail_id),
    FOREIGN KEY (trail_feature_id) REFERENCES CW2.Feature(trail_feature_id)
);

-- Create the LocationPoint table under CW2 schema
CREATE TABLE CW2.LocationPoint (
    location_point_id INT PRIMARY KEY,
    longitude DECIMAL(9,6) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    description VARCHAR(255)
);

-- Create the TrailPoints table linking Trail and LocationPoint under CW2 schema
CREATE TABLE CW2.TrailPoints (
    trail_id INT,
    location_point_id INT,
    sequenceNumber INT,
    PRIMARY KEY (trail_id, location_point_id),
    FOREIGN KEY (trail_id) REFERENCES CW2.Trail(trail_id),
    FOREIGN KEY (location_point_id) REFERENCES CW2.LocationPoint(location_point_id)
);





-- Sample Data --

-- Insert data into the Owner table
INSERT INTO CW2.Owner (owner_id, owner_name, email, is_admin)
VALUES
(1, 'John Doe', 'john.doe@example.com', 1),
(2, 'Jane Smith', 'jane.smith@example.com', 0);

-- Insert data into the RouteType table
INSERT INTO CW2.RouteType (route_id, route_type)
VALUES
(1, 'Loop'),
(2, 'Out-and-back');

-- Insert data into the Feature table
INSERT INTO CW2.Feature (trail_feature_id, trail_feature)
VALUES
(1, 'Scenic View'),
(2, 'Waterfall'),
(3, 'Wildlife Sightings');

-- Insert data into the Trail table
INSERT INTO CW2.Trail (trail_id, name, difficulty, location, length, elevation_gain, description, owner_id, route_id)
VALUES
(1, 'Mountain View Trail', 'Moderate', 'Mountain Park', 5.5, 400.00, 'A beautiful trail with scenic views.', 1, 1),
(2, 'Riverfront Trail', 'Easy', 'Riverside Park', 3.2, 100.00, 'A relaxing trail along the river.', 2, 2);

-- Insert data into the Trail_Feature join table
INSERT INTO CW2.Trail_Feature (trail_id, trail_feature_id)
VALUES
(1, 1),  -- Mountain View Trail has Scenic View
(1, 2),  -- Mountain View Trail has Waterfall
(2, 3);  -- Riverfront Trail has Wildlife Sightings

-- Insert data into the LocationPoint table
INSERT INTO CW2.LocationPoint (location_point_id, longitude, latitude, description)
VALUES
(1, -122.4194, 37.7749, 'Start point of the trail'),
(2, -122.4148, 37.7799, 'Viewpoint with scenic views'),
(3, -122.4080, 37.7850, 'Waterfall location');

-- Insert data into the TrailPoints table
INSERT INTO CW2.TrailPoints (trail_id, location_point_id, sequenceNumber)
VALUES
(1, 1, 1),  -- Mountain View Trail, Start point
(1, 2, 2),  -- Mountain View Trail, Scenic View
(1, 3, 3),  -- Mountain View Trail, Waterfall
(2, 1, 1),  -- Riverfront Trail, Start point
(2, 2, 2);  -- Riverfront Trail, Wildlife Sightings

