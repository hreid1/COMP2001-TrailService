-- Tables 
    -- owners
        -- owner_id INT PK AUTO_INCREMENT
        -- owner_name VARCHAR(255)
        -- email VARCHAR(255)
        -- is_admin VARCHAR(50)
    -- route_type
        -- route_id INT PK AUTO_INCREMENT
        -- route_type VARCHAR(50)
    -- trails
        -- trail_id INT PK AUTO_INCREMENT
        -- owner_id INT FK owners(owner_id)
        -- route_id INT FK route_type(route_id)
        -- name VARCHAR(255)
        -- difficulty VARCHAR(50)
        -- location VARCHAR(255)
        -- length DECIMAL(6,2)
        -- elevation_gain DECIMAL(6,2)
        -- description TEXT
    -- trail_features JOIN TABLE (trail_id, feature_id)
        -- trail_id INT FK trails(trail_id)
        -- feature_id INT FK feature(feature_id)
    -- feature
        -- feature_id INT PK AUTO_INCREMENT
        -- feature_name VARCHAR(255)
    -- location_point
        -- location_point_id INT PK AUTO_INCREMENT
        -- longitude DECIMAL(9,6)
        -- latitude DECIMAL(9,6)
        -- description TEXT
    -- trail_points JOIN TABLE (trail_id, location_point_id)
        -- trail_id INT FK trails(trail_id)
        -- location_point_id INT FK location_point(location_point_id)
        -- sequenceNumber INT 

drop table if exists CW2.trail_points;
drop table if exists CW2.location_point;
drop table if exists CW2.trail_features;
drop table if exists CW2.feature;
drop table if exists CW2.trails;
drop table if exists CW2.route_type;
drop table if exists CW2.owners;

drop schema if exists CW2;

GO
create schema CW2;
GO

create table CW2.owners (
    owner_id int primary key identity(1,1),
    owner_name varchar(50) not null,
    email varchar(100) not null unique,
    role varchar(50) not null check (role in ('Admin', 'User'))
);
GO

create table CW2.route_type (
    route_id int primary key identity(1,1),
    route_type varchar(50) not null
);
GO

create table CW2.trails (
    trail_id int primary key identity(1,1),
    owner_id int not null references CW2.owners(owner_id),
    route_id int not null references CW2.route_type(route_id),
    name varchar(255) not null,
    difficulty varchar(50) not null,
    location varchar(255) not null,
    length decimal(6,2) not null,
    elevation_gain decimal(6,2) not null,
    description text not null
);
GO

create table CW2.feature (
    feature_id int primary key identity(1,1),
    feature_name varchar(255) not null
);

create table CW2.trail_features (
    trail_id int not null references CW2.trails(trail_id),
    feature_id int not null references CW2.feature(feature_id),
    primary key (trail_id, feature_id)
);

create table CW2.location_point (
    location_point_id int primary key identity(1,1),
    longitude decimal(9,6) not null,
    latitude decimal(9,6) not null,
    description text not null
);

create table CW2.trail_points (
    trail_id int not null references CW2.trails(trail_id),
    location_point_id int not null references CW2.location_point(location_point_id),
    sequence_number int not null,
    primary key (trail_id, location_point_id)
);
GO

-- Insert data

-- Owners
    -- Name: Grace Hopper
        -- Email: grace@plymouth.ac.uk
        -- Password: ISAD123!
        -- Role: Admin
    -- Name: Tim Berners-Lee
        -- Email: tim@plymouth.ac.uk
        -- Password: COMP2001!
        -- Role: User
    -- Name: Ada Lovelace
        -- Email: ada@plymouth.ac.uk
        -- Password: insecurePassword
        -- Role: User

-- Route Types
    -- Loop
    -- Out and Back
    -- Point to Point

-- Trails
    -- Name: Plymbridge Circular
        -- Owner: Grace Hopper
        -- Route Type: Loop
        -- Difficulty: Easy
        -- Location: Plymbridge Woods
        -- Length: 5.00 miles
        -- Elevation Gain: 100.00 metres
        -- Description: A circular walk around Plymbridge Woods
    -- Name: Plymouth Waterfront
        -- Owner: Tim Berners-Lee
        -- Route Type: Out and Back
        -- Difficulty: Moderate
        -- Location: Plymouth Hoe
        -- Length: 10.00 miles
        -- Elevation Gain: 200.00 metres
        -- Description: A walk along the waterfront with views of the sea

-- Features
    -- Waterfall
    -- Scenic View
    -- Wildlife

-- TrailFeatures
    -- Plymbridge Circular: Waterfall
    -- Plymouth Waterfront: Scenic View

-- Location Points
    -- Point A: -123.3656, 48.4284
    -- Point B: -123.3657, 48.4285
    -- Point C: -123.3658, 48.4286
    -- Point D: -123.3659, 48.4287
    -- Point E: -123.3660, 48.4288
    -- Point F: -123.3661, 48.4289
    -- Point G: -123.3662, 48.4290
    -- Point H: -123.3663, 48.4291
    -- Point I: -123.3664, 48.4292
    -- Point J: -123.3665, 48.4293
    -- Point K: -123.3666, 48.4294
    -- Point L: -123.3667, 48.4295
    -- Point M: -123.3668, 48.4296
    -- Point N: -123.3669, 48.4297
    -- Point O: -123.3670, 48.4298

-- Trail Points
    -- Plymbridge Circular
        -- Point A
        -- Point B
        -- Point C
        -- Point D
        -- Point E
        -- Point K
        -- Point L
        -- Point M
        -- Point N
        -- Point O
    -- Plymouth Waterfront
        -- Point F
        -- Point G
        -- Point H
        -- Point I
        -- Point J

-- Trail Points
    -- Plymbridge Circular
        -- Point A
        -- Point B
        -- Point C
        -- Point D
        -- Point E
        -- Point K
        -- Point L
        -- Point M
        -- Point N
        -- Point O
    -- Plymouth Waterfront
        -- Point F
        -- Point G
        -- Point H
        -- Point I
        -- Point J

-- Insert sample data for owners
INSERT INTO CW2.owners (owner_name, email, role) VALUES
('Grace Hopper', 'grace@plymouth.ac.uk', 'ADMIN'), -- Admin
('Tim Berners-Lee', 'tim@plymouth.ac.uk', 'USER'), -- User
('Ada Lovelace', 'ada@plymouth.ac.uk', 'USER'); -- User
GO

-- Insert sample data for route types
INSERT INTO CW2.route_type (route_type) VALUES
('Loop'),
('Out and Back'),
('Point to Point');
GO

-- Insert sample data for trails
INSERT INTO CW2.trails (owner_id, route_id, name, difficulty, location, length, elevation_gain, description) VALUES
(1, 1, 'Plymbridge Circular', 'Easy', 'Plymbridge Woods', 5.00, 100.00, 'A circular walk around Plymbridge Woods'),
(2, 2, 'Plymouth Waterfront', 'Moderate', 'Plymouth Hoe', 10.00, 200.00, 'A walk along the waterfront with views of the sea');
GO

-- Insert sample data for features
INSERT INTO CW2.feature (feature_name) VALUES
('Waterfall'),
('Scenic View'),
('Wildlife');
GO

-- Insert sample data for trail_features (many-to-many relation between trails and features)
INSERT INTO CW2.trail_features (trail_id, feature_id) VALUES
(1, 1), -- Plymbridge Circular has Waterfall
(2, 2); -- Plymouth Waterfront has Scenic View
GO

-- Insert sample data for location_points (coordinates for the points)
INSERT INTO CW2.location_point (longitude, latitude, description) VALUES
(-123.3656, 48.4284, 'Point A'),
(-123.3657, 48.4285, 'Point B'),
(-123.3658, 48.4286, 'Point C'),
(-123.3659, 48.4287, 'Point D'),
(-123.3660, 48.4288, 'Point E'),
(-123.3661, 48.4289, 'Point F'),
(-123.3662, 48.4290, 'Point G'),
(-123.3663, 48.4291, 'Point H'),
(-123.3664, 48.4292, 'Point I'),
(-123.3665, 48.4293, 'Point J'),
(-123.3666, 48.4294, 'Point K'),
(-123.3667, 48.4295, 'Point L'),
(-123.3668, 48.4296, 'Point M'),
(-123.3669, 48.4297, 'Point N'),
(-123.3670, 48.4298, 'Point O');
GO

-- Insert sample data for trail_points (many-to-many relation between trails and location points)
INSERT INTO CW2.trail_points (trail_id, location_point_id, sequence_number) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 4),
(1, 5, 5),
(1, 11, 6),
(1, 12, 7),
(1, 13, 8),
(1, 14, 9),
(1, 15, 10),
(2, 6, 1),
(2, 7, 2),
(2, 8, 3),
(2, 9, 4),
(2, 10, 5);
GO
