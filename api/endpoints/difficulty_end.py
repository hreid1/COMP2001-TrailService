from flask import abort, make_response
from config import db
from models import Difficulty, difficulty_schema, difficulties_schema

def read_all():
    difficulties = Difficulty.query.order_by(Difficulty.difficultyName).all()
    difficulties = difficulties_schema.dump(difficulties)
    return difficulties

def read_one(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    if difficulty is not None:
        difficulty = difficulty_schema.dump(difficulty)
    else:
        abort(404, f'Difficulty not found for Id: {difficulty_id}')
    return difficulty

def create(difficulty):
    difficultyName = difficulty.get('difficultyName')
    existing_difficulty = Difficulty.query.filter(Difficulty.difficultyName == difficultyName).one_or_none()
    if existing_difficulty is None:
        new_difficulty = Difficulty(difficultyName=difficultyName)
        db.session.add(new_difficulty)
        db.session.commit()
        return difficulty_schema.dump(new_difficulty), 201
    else:
        abort(409, f'Difficulty {difficultyName} exists already')

def update(difficulty_id, difficulty):
    update_difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    if update_difficulty is not None:
        difficulty_schema.load(difficulty, session=db.session)
        db.session.commit()
        return difficulty_schema.dump(update_difficulty), 200
    else:
        abort(404, f'Difficulty not found for Id: {difficulty_id}')

def delete(difficulty_id):
    difficulty = Difficulty.query.filter(Difficulty.id == difficulty_id).one_or_none()
    if difficulty is not None:
        db.session.delete(difficulty)
        db.session.commit()
        return make_response(f'Difficulty {difficulty_id} deleted', 204)
    else:
        abort(404, f'Difficulty not found for Id: {difficulty_id}')

         