from flask import Flask, render_template, jsonify, request, abort
import config
from auth import get_owner_by_email, authenticate_user


app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,debug=True)
