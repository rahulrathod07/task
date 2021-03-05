from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
app.secret_key = "Hello-guys-this-is-super-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminrahul:password@db4free.net:3306/fyndimdb'

db = SQLAlchemy(app)

users = {
    'admin': [generate_password_hash('admin', method='sha256'), True],
    'user': [generate_password_hash('user', method='sha256'), False],
    'Harsh': [generate_password_hash('12345', method='sha256'), False]
}


# Table attribute connection class
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    imdb_score = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(80), nullable=False)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name,
            "director": self.director,
            "genre": self.genre.split(","),
            "99popularity": self.popularity,
            "imdb_score": self.imdb_score
        }


# Decorator for token decoding and user info gathering
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!!'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # current_user = User.query.filter_by(public_id=data['public_id']).first()
            current_user = data['sub']

        except:
            return jsonify({'message': 'Invalid Token!!  Login Again.'})

        return f(current_user, *args, **kwargs)

    return decorated


# Home page
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to IMDB Task page. Login to perform operations.'})


# See all movies in database
@app.route('/movies', methods=['GET'])
@token_required
def get_all_movies(current_user):
    movies = Movies.query.all()

    return jsonify([movie.serialized for movie in movies])


# Get movie by id
@app.route('/movies/<id>', methods=['GET'])
@token_required
def get_one_movie(current_user, id):
    movie = Movies.query.filter_by(id=id).first()

    return jsonify([movie.serialized])


# Add new movies
@app.route('/movies', methods=['POST'])
@token_required
def add_movie(current_user):
    if not users[current_user][1]:
        return jsonify({'message': 'You are not allowed to perform this action!!'})

    data = request.get_json()

    new_movie = Movies(popularity=data['99popularity'], director=data['director'], genre=data['genre'],
                       imdb_score=data['imdb_score'], name=data['name'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'New Movie added successfully.', 'movie': data})


# Modify movie details
@app.route('/movies/<id>', methods=['PUT'])
@token_required
def modify_movie_data(current_user, id):
    if not users[current_user][1]:
        return jsonify({'message': 'You are not allowed to perform this action!!'})

    movie = Movies.query.filter_by(id=id).first()

    if not movie:
        return jsonify({'message': 'No Movie found for entered id!!'})
    else:
        data = request.get_json()

        movie.name = data['name']
        movie.popularity = data['99popularity']
        movie.director = data['director']
        movie.genre = data['genre']
        movie.imdb_score = data['imdb_score']

        db.session.commit()
        return jsonify({'message': 'Movie data updated successfully.', 'movie': data})


# Delete movies
@app.route('/movies/<id>', methods=['DELETE'])
@token_required
def delete_movie(current_user, id):
    if not users[current_user][1]:
        return jsonify({'message': 'You are not allowed to perform this action!!'})

    movie = Movies.query.filter_by(id=id).first()

    if not movie:
        return jsonify({'message': 'No Movie found for entered id!!'})
    else:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie is Deleted successfully.'})


# Search movies by id, movie_name, genre,director, popularity and imdb_score
@app.route('/search', methods=['GET'])
@token_required
def search_movie(current_user):
    movies = None

    name = request.args.get('name')
    if name:
        movies = Movies.query.filter_by(name=name).all()

    if not movies:
        return jsonify({"message": "No movies found"})
    return jsonify({"movies": [movie.serialized for movie in movies]})


# Login user and token generation
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify!! Please enter all the required details to login.'})

    user = auth.username

    if user not in users.keys():
        return jsonify({'message': 'Username not exist'})
    elif check_password_hash(users[user][0], auth.password):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'iat': datetime.utcnow(),
            'sub': user
        }
        return jsonify({'token': jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')})
    else:
        return jsonify({'message': 'You have entered wrong password!'})


if __name__ == '__main__':
    app.debug = True
    app.run()
