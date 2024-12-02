from flask import Flask, jsonify
from database import connex_app, db
from endpoints import register_routes

# Initialize Flask and Connexion app
app = connex_app.app

# Swagger integration 
#connex_app.add_api('swagger.yml') 

# Register endponts
register_routes(app)


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Trail Service API"})

# Start the application
if __name__ == "__main__":
    # Ensure the app is running in debug mode (if required)
    app.run(host="0.0.0.0", port=8000, debug=True)
