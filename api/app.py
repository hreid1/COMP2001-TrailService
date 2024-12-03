from flask import Flask, render_template, jsonify, request
import config
from models import Trail, trails_schema
from trails import read_all, read_one, create, update, delete

app = config.connex_app
#app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/trails', methods=['GET'])
def get_trails():
    return read_all()

@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    return read_one(trail_id)

@app.route('/trails', methods=['POST'])
def add_trail():
    trail = request.get_json()
    return create(trail)

@app.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    trail = request.get_json()
    return update(trail_id, trail)

@app.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    return delete(trail_id)
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
