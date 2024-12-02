from flask import abort, make_response, jsonify
from api.database.config import db
from models import Difficulty, difficulty_schema, difficulties_schema

# Get all difficulties
def read_all():
    difficulties = Difficulty.query.order_by(Difficulty.difficultyName).all()
    return difficulties_schema.dump(difficulties)

# Get one difficulty by ID
def read_one(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    if difficulty:
        return difficulty_schema.dump(difficulty)
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')

# Create a new difficulty
def create(difficulty_data):
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
            abort(500, description="An error occurred while creating difficulty")
        return difficulty_schema.dump(new_difficulty), 201  # Created response
    else:
        abort(409, description=f'Difficulty {difficultyName} already exists')

# Update an existing difficulty
def update(difficulty_id, difficulty_data):
    update_difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    
    if update_difficulty:
        difficultyName = difficulty_data.get('difficultyName', update_difficulty.difficultyName)
        
        if not difficultyName:
            abort(400, description='Difficulty name cannot be empty')

        update_difficulty.difficultyName = difficultyName
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description="An error occurred while updating difficulty")

        return difficulty_schema.dump(update_difficulty), 200  # OK response
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')

# Delete a difficulty
def delete(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    
    if difficulty:
        db.session.delete(difficulty)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description="An error occurred while deleting difficulty")
        return make_response(f'Difficulty {difficulty_id} deleted', 204)  # No content response
    else:
        abort(404, description=f'Difficulty not found for Id: {difficulty_id}')
