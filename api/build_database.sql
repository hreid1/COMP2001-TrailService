-- Tables 
    -- owners
        -- owner_id INT PK AUTO_INCREMENT
        -- owner_name VARCHAR(255)
        -- email VARCHAR(255)
        -- is_admin BOOLEAN
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

drop table if exists CW2.feature;
drop table if exists CW2.trail_points;
drop table if exists CW2.location_point;
drop table if exists CW2.trail_features;
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
    role BIT not null
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
    sequenceNumber int not null,
    primary key (trail_id, location_point_id)
);
GO

-- Insert data

-- Insert sample data into the Owner table
INSERT INTO CW2.owners (owner_name, email, role) VALUES
('John Doe', 'john.doe@example.com', 1),
('Jane Smith', 'jane.smith@example.com', 0);
GO

-- Insert sample data into the RouteType table
INSERT INTO CW2.route_type (route_type) VALUES
('Loop'),
('Out and Back');
GO

-- Insert sample data into the Trail table
INSERT INTO CW2.trails (owner_id, route_id, name, difficulty, location, length, elevation_gain, description) VALUES
(1, 1, 'Trail A', 'Easy', 'Location A', 5.00, 100.00, 'Description A'),
(2, 2, 'Trail B', 'Moderate', 'Location B', 10.00, 200.00, 'Description B');
GO

-- Insert sample data into the Feature table
INSERT INTO CW2.feature (feature_name) VALUES
('Waterfall'),
('Scenic View');
GO

-- Insert sample data into the TrailFeature join table
INSERT INTO CW2.trail_features (trail_id, feature_id) VALUES
(1, 1),
(2, 2);
GO

-- Insert sample data into the LocationPoint table
INSERT INTO CW2.location_point (longitude, latitude, description) VALUES
(-123.3656, 48.4284, 'Point A'),
(-123.3657, 48.4285, 'Point B');
GO

-- Insert sample data into the TrailPoints join table
INSERT INTO CW2.trail_points (trail_id, location_point_id, sequenceNumber) VALUES
(1, 1, 1),
(1, 2, 2);
GO


