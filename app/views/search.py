from app import app
from app.auth import token_required, admin_required
from app import db
from app.models import Movies
from flask import jsonify, request


# Search movies
@app.route('/search', methods=['GET'])
@token_required
def search_movie(current_user):
    filters = []
    name = request.args.get('name')
    if name:
        criteria = '%{}%'.format(name)
        filters.append(Movies.name.like(criteria))
    director = request.args.get('director')
    if director:
        criteria = '%{}%'.format(director)
        filters.append(Movies.director.like(criteria))
    imdb_score = request.args.get('imdb_score')
    if imdb_score:
        filters.append(Movies.popularity >= imdb_score)
    popularity = request.args.get('99popularity')
    if popularity:
        filters.append(Movies.popularity >= popularity)
    genre = request.args.get('genre')
    if genre:
        sanitized_genres = [x.lower().strip() for x in genre.split(',')]
        for x in sanitized_genres:
            filters.append(Movies.genres.any(name=x))
    movies = Movies.query.filter(*filters).all()
    if not movies:
        return jsonify({'message': 'No movies found.', 'movies': movies})
    return jsonify({'message': 'Movies filtered successfully.', 'movies': [movie.serialized for movie in movies]})
