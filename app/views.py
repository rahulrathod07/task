from app import app, jwt, os, jsonify, request, check_password_hash
from app.auth import token_required, admin_required
from app.models import Users, Movies
from app.config import db


# Login user and token generation
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify. Please enter all the required details to login.'}), 401
    user = Users.query.filter_by(name=auth.username).first()
    if not user:
        return jsonify({'message': 'Username does not exist.'}), 401
    elif check_password_hash(user.password, auth.password):
        payload = {
            'user': user.serialized
        }
        return jsonify({'token': jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')})
    return jsonify({'message': 'You have entered wrong password.'}), 401


# Home page
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to IMDB Task page.'})


# Get all movies
@app.route('/movies', methods=['GET'])
@token_required
def get_all_movies(current_user):
    movies = Movies.query.all()
    # f.director()
    return jsonify({'message': 'Fetched all movies successfully.', 'movies': [movie.serialized for movie in movies]})


# Get movie by id
@app.route('/movies/<id>', methods=['GET'])
@token_required
def get_one_movie(current_user, id):
    movie = Movies.query.get(id)
    if not movie:
        return jsonify({'message': 'No movie found for entered id.'}), 404
    return jsonify({'message': 'Fetched movie by id successfully.', 'movie': movie.serialized})


# Add new movie
@app.route('/movies', methods=['POST'])
@token_required
@admin_required
def add_movie(current_user):
    data = request.get_json()
    movie = Movies.query.filter_by(name=data['name']).first()
    if movie:
        return jsonify({'message': 'Movie already exist.'}), 409
    new_movie = Movies(
        popularity=data['99popularity'],
        director=data['director'],
        genre=','.join([x.strip() for x in data['genre']]),
        imdb_score=data['imdb_score'],
        name=data['name']
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'New movie added successfully.', 'movie': new_movie.serialized})


# Update movie
@app.route('/movies/<id>', methods=['PUT'])
@token_required
@admin_required
def update_movie(current_user, id):
    movie = Movies.query.get(id)
    if not movie:
        return jsonify({'message': 'No movie found for entered id.'}), 404
    data = request.get_json()
    movie.name = data['name']
    movie.popularity = data['99popularity']
    movie.director = data['director']
    movie.genre = ','.join([x.strip() for x in data['genre']])
    movie.imdb_score = data['imdb_score']
    db.session.commit()
    return jsonify({'message': 'Movie data updated successfully.', 'movie': movie.serialized})


# Delete movie
@app.route('/movies/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_movie(current_user, id):
    movie = Movies.query.get(id)
    if not movie:
        return jsonify({'message': 'No movie found for entered id.'}), 404
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie is deleted successfully.', 'movie': movie.serialized})


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
        for x in genre.split(','):
            criteria = '%{}%'.format(x)
            filters.append(Movies.genre.like(criteria))
    movies = Movies.query.filter(*filters).all()
    if not movies:
        return jsonify({'message': 'No movies found.', 'movies': movies})
    return jsonify({'message': 'Movies filtered successfully.', 'movies': [movie.serialized for movie in movies]})