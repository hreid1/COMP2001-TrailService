import pyodbc

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'  # Corrected server name
    'DATABASE=master;' 
    'UID=SA;'
    'PWD=C0mp2001!;'
    'Connection Timeout=30;'
    'Trusted_Connection=No'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Verify current database
    cursor.execute("SELECT DB_NAME()")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")

    # Verify current user
    cursor.execute("SELECT USER_NAME()")
    current_user = cursor.fetchone()
    print(f"Connected as user: {current_user[0]}")

    # Create table
    cursor.execute(''' 
        CREATE TABLE Owner (
            ownerID INT PRIMARY KEY,
            ownerName VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            isAdmin BIT  -- Corrected BOOLEAN to BIT
        )
    ''')

    # Insert data
    owners = [
        (1, 'John Doe', 'john.doe@example.com', 1),
        (2, 'Jane Smith', 'jane.smith@example.com', 0),
        (3, 'Mike Johnson', 'mike.johnson@example.com', 0)
    ]
    cursor.executemany('INSERT INTO Owner (ownerID, ownerName, email, isAdmin) VALUES (?, ?, ?, ?)', owners)

    # Commit the changes
    conn.commit()

    # Fetch data
    cursor.execute('SELECT * FROM Owner')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except pyodbc.Error as e:
    print(f"Error: {e}")

finally:
    if 'conn' in locals():
        cursor.execute('DROP TABLE Owner')  # Drop the correct table
        conn.close()
