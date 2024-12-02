import connexion
from flask import jsonify
from database.config import connex_app, db
from models.trail import Trail, trails_schema

# Initialize Flask and Connexion app
app = connex_app.app

# Swagger integration 
connex_app.add_api('swagger.yml') 

@app.route("/")
def home():
    try:
        # Query the database for all trails
        trails = Trail.query.all()

        # Serialize the list of trails using TrailSchema
        trails_json = trails_schema.dump(trails)

        # Return the serialized list as a JSON response
        return jsonify(trails_json)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the application
if __name__ == "__main__":
    # Ensure the app is running in debug mode (if required)
    app.run(host="0.0.0.0", port=8000, debug=True)