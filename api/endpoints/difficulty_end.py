from flask import abort, make_response, jsonify, request
from database import db
from models import Difficulty, difficulty_schema, difficulties_schema

# Get all difficulties
def read_all():
    difficulties = Difficulty.query.order_by(Difficulty.difficultyName).all()
    return difficulties_schema.dump(difficulties)

# Get one difficulty by ID
def read_one(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.difficultyID == difficulty_id).one_or_none()
    if difficulty:
        return difficulty_schema.dump(difficulty)
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')

# Create a new difficulty
def create():
    difficulty_data = request.get_json()
    difficultyName = difficulty_data.get('difficultyName')
    
    if not difficultyName:
        abort(400, description='Difficulty name is required')

    existing_difficulty = Difficulty.query.filter(Difficulty.difficultyName == difficultyName).one_or_none()
    
    if existing_difficulty is None:
        new_difficulty = Difficulty(difficultyName=difficultyName)
        db.session.add(new_difficulty)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error creating difficulty: {str(e)}')
        return difficulty_schema.dump(new_difficulty), 201
    else:
        abort(409, description=f'Difficulty with name {difficultyName} already exists')

# Update an existing difficulty
def update(difficulty_id):
    difficulty_data = request.get_json()
    difficulty = Difficulty.query.filter(Difficulty.difficultyID == difficulty_id).one_or_none()
    
    if difficulty:
        difficulty.difficultyName = difficulty_data.get('difficultyName', difficulty.difficultyName)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error updating difficulty: {str(e)}')
        return difficulty_schema.dump(difficulty)
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')

# Delete a difficulty
def delete(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.difficultyID == difficulty_id).one_or_none()
    
    if difficulty:
        try:
            db.session.delete(difficulty)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f'Error deleting difficulty: {str(e)}')
        return make_response(jsonify({"message": "Difficulty deleted successfully"}), 204)
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')

