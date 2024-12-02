import pyodbc

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=TrailTest;'
    'UID=SA;'
    'PWD=C0mp2001!;'
    'TrustServerCertificate=yes;'
    'Encrypt=yes;'
)

def create_tables():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(''' 
            CREATE TABLE Owner (
                ownerID INT PRIMARY KEY,
                ownerName VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                isAdmin BIT
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE Difficulty (
                difficultyID INT PRIMARY KEY,
                difficultyName VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE RouteType (
                routeTypeID INT PRIMARY KEY,
                routeTypeName VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE Location (
                locationID INT PRIMARY KEY,
                locationName VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE Trail (
                id INT PRIMARY KEY,
                trailName VARCHAR(255) NOT NULL UNIQUE,
                rating NUMERIC(3, 2) CHECK (rating >= 0 AND rating <= 5),
                trailDescription TEXT,
                trailDistance NUMERIC(6, 2),
                trailElevationGain NUMERIC(6, 2),
                averageTimeToComplete NUMERIC(5, 2),
                difficultyID INT FOREIGN KEY REFERENCES Difficulty(difficultyID),
                routeTypeID INT FOREIGN KEY REFERENCES RouteType(routeTypeID),
                locationID INT FOREIGN KEY REFERENCES Location(locationID),
                ownerID INT FOREIGN KEY REFERENCES Owner(ownerID)
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE TrailFeature (
                featureID INT PRIMARY KEY,
                featureName VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE LocationPoint (
                pointID INT PRIMARY KEY,
                locationID INT FOREIGN KEY REFERENCES Location(locationID),
                latitude NUMERIC(9, 6),
                longitude NUMERIC(9, 6)
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE TrailFeatureJoin (
                id INT PRIMARY KEY,
                trailID INT FOREIGN KEY REFERENCES Trail(id),
                featureID INT FOREIGN KEY REFERENCES TrailFeature(featureID)
            )
        ''')

        conn.commit()
        print("Tables created successfully.")

    except pyodbc.Error as e:
        print(f"Error: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

def insert_data():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insert data into Owner table
        owners = [
            (1, 'John Doe', 'john.doe@example.com', 1),
            (2, 'Jane Smith', 'jane.smith@example.com', 0),
            (3, 'Mike Johnson', 'mike.johnson@example.com', 0)
        ]
        cursor.executemany('INSERT INTO Owner (ownerID, ownerName, email, isAdmin) VALUES (?, ?, ?, ?)', owners)

        # Insert data into Difficulty table
        difficulties = [
            (1, 'Easy'),
            (2, 'Moderate'),
            (3, 'Hard')
        ]
        cursor.executemany('INSERT INTO Difficulty (difficultyID, difficultyName) VALUES (?, ?)', difficulties)

        # Insert data into RouteType table
        route_types = [
            (1, 'Loop'),
            (2, 'Out and Back'),
            (3, 'Point to Point')
        ]
        cursor.executemany('INSERT INTO RouteType (routeTypeID, routeTypeName) VALUES (?, ?)', route_types)

        # Insert data into Location table
        locations = [
            (1, 'Location A'),
            (2, 'Location B'),
            (3, 'Location C')
        ]
        cursor.executemany('INSERT INTO Location (locationID, locationName) VALUES (?, ?)', locations)

        # Insert data into Trail table
        trails = [
            (1, 'Trail 1', 4.5, 'Beautiful trail', 10.5, 500, 3.5, 1, 1, 1, 1),
            (2, 'Trail 2', 3.8, 'Challenging trail', 8.2, 300, 2.8, 2, 2, 2, 2),
            (3, 'Trail 3', 4.2, 'Scenic trail', 12.0, 600, 4.0, 3, 3, 3, 3)
        ]
        cursor.executemany('INSERT INTO Trail (id, trailName, rating, trailDescription, trailDistance, trailElevationGain, averageTimeToComplete, difficultyID, routeTypeID, locationID, ownerID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', trails)

        # Insert data into TrailFeature table
        features = [
            (1, 'Waterfall'),
            (2, 'Cave'),
            (3, 'Scenic View')
        ]
        cursor.executemany('INSERT INTO TrailFeature (featureID, featureName) VALUES (?, ?)', features)

        # Insert data into LocationPoint table
        location_points = [
            (1, 1, 34.052235, -118.243683),
            (2, 2, 36.169941, -115.139832),
            (3, 3, 40.712776, -74.005974)
        ]
        cursor.executemany('INSERT INTO LocationPoint (pointID, locationID, latitude, longitude) VALUES (?, ?, ?, ?)', location_points)

        # Insert data into TrailFeatureJoin table
        trail_feature_joins = [
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 3)
        ]
        cursor.executemany('INSERT INTO TrailFeatureJoin (id, trailID, featureID) VALUES (?, ?, ?)', trail_feature_joins)

        conn.commit()
        print("Data inserted successfully.")

    except pyodbc.Error as e:
        print(f"Error: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_data()