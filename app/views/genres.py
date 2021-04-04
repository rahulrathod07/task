from app import app
from app.auth import token_required, admin_required
from app import db
from app.models import Movies, Genres, MovieGenres
from flask import jsonify, request


# Get all genres
@app.route('/genres', methods=['GET'])
@token_required
def get_all_genres(current_user):
    genres = Genres.query.all()
    return jsonify({'message': 'Fetched all genres successfully.', 'genres': [genre.serialized for genre in genres]})


# Get genre by id
@app.route('/genres/<id>', methods=['GET'])
@token_required
def get_genre(current_user, id):
    genre = Genres.query.get(id)
    if not genre:
        return jsonify({'message': 'No genre found for entered id.'}), 404
    return jsonify({'message': 'Fetched genre by id successfully.', 'genre': genre.serialized})


# Add new genre
@app.route('/genres', methods=['POST'])
@token_required
@admin_required
def add_genre(current_user):
    data = request.get_json()
    genre = Genres.query.filter_by(name=data['name']).first()
    if genre:
        return jsonify({'message': 'Genre already exist.'}), 409
    new_genre = Genres(
        name=data['name'],
        description=data['description'],
    )
    db.session.add(new_genre)
    db.session.commit()
    return jsonify({'message': 'New genre added successfully.', 'genre': new_genre.serialized})


# Update genre
@app.route('/genres/<id>', methods=['PUT'])
@token_required
@admin_required
def update_genre(current_user, id):
    genre = Genres.query.get(id)
    if not genre:
        return jsonify({'message': 'No genre found for entered id.'}), 404
    data = request.get_json()
    genre.name = data['name'].lower().strip()
    genre.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Genre data updated successfully.', 'genre': genre.serialized})


# Delete genre
@app.route('/genres/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_genre(current_user, id):
    genre = Genres.query.get(id)
    if not genre:
        return jsonify({'message': 'No genre found for entered id.'}), 404
    serialized = genre.serialized
    db.session.delete(genre)
    db.session.commit()
    return jsonify({'message': 'Genre is deleted successfully.', 'genre': serialized})
