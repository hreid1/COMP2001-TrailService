from flask import render_template
# from endpoints import register_routes

from database.config import config
from .models import Trail

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

# register_routes(app)

@app.route("/")
def home():
    trail = Trail.query.all()
    return render_template("home.html", trail=trail)

if __name__ == "__main__":
    # Check the database connection before starting the app
    config.check_db_connection()
    app.run(host="0.0.0.0", port=8000, debug=True)
