CREATE TABLE Owner (
    ownerID INT PRIMARY KEY,
    ownerName VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    isAdmin BOOLEAN
);

CREATE TABLE Difficulty (
    difficultyID INT PRIMARY KEY,
    difficultyName VARCHAR(50) NOT NULL
);

CREATE TABLE RouteType (
    routeTypeID INT PRIMARY KEY,
    routeTypeName VARCHAR(50) NOT NULL
);

CREATE TABLE Location (
    locationID INT PRIMARY KEY,
    locationName VARCHAR(255) NOT NULL
);

CREATE TABLE Trail (
    trailID INT PRIMARY KEY,
    trailName VARCHAR(255) NOT NULL,
    rating DECIMAL(3,2) CHECK (rating >= 0 AND rating <= 5),
    difficultyID INT,
    routeTypeID INT,
    locationID INT,
    trailDescription TEXT,
    trailDistance DECIMAL(6,2),
    trailElevationGain DECIMAL(6,2),
    averageTimeToComplete DECIMAL(5,2),
    ownerID INT,
    FOREIGN KEY (difficultyID) REFERENCES Difficulty(difficultyID),
    FOREIGN KEY (routeTypeID) REFERENCES RouteType(routeTypeID),
    FOREIGN KEY (locationID) REFERENCES Location(locationID),
    FOREIGN KEY (ownerID) REFERENCES Owner(ownerID)
);

CREATE TABLE TrailFeature (
    featureID INT PRIMARY KEY,
    featureName VARCHAR(255) NOT NULL
);

CREATE TABLE TrailFeatureJoin (
    trailID INT,
    featureID INT,
    PRIMARY KEY (trailID, featureID),
    FOREIGN KEY (trailID) REFERENCES Trail(trailID),
    FOREIGN KEY (featureID) REFERENCES TrailFeature(featureID)
);

CREATE TABLE LocationPoint (
    locationPointID INT PRIMARY KEY,
    trailID INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    sequenceNumber INT,
    FOREIGN KEY (trailID) REFERENCES Trail(trailID)
);
