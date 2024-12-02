# app.py

import connexion
from flask import jsonify
from models import Trail  # Make sure you have this model defined
from config import connex_app, db  # Import the connex_app and db from config.py

# Initialize Flask and Connexion app
app = connex_app.app

# Swagger integration 
connex_app.add_api('swagger.yml') 

@app.route("/")
def home():
    try:
        # Query the database for all trails
        trails = Trail.query.all()

        # Convert to a list of dictionaries (customize based on your model)
        trails_list = [{"trailName": trail.trailName, "rating": trail.rating} for trail in trails]

        # Return the list as a JSON response
        return jsonify(trails_list)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the application
if __name__ == "__main__":
    # Ensure the app is running in debug mode (if required)
    app.run(host="0.0.0.0", port=8000, debug=True)
