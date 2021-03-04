from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
app.secret_key = "Hello-guys-this-is-super-secret-key"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminrahul:password@db4free.net:3306/fyndimdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b8d20ec0f53090:46cce531@us-cdbr-east-03.cleardb.com:3306/taskimdb'

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
    movie_name = db.Column(db.String(80), nullable=False)


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


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to IMDB Task page. Login to perform operations.'})


@app.route('/movies', methods=['GET'])
@token_required
def get_all_movies(current_user):
    movies = Movies.query.all()

    output = []

    for movie in movies:
        movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                      'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
        output.append(movie_data)

    return jsonify({'Movies': output})


@app.route('/movies', methods=['POST'])
@token_required
def add_movie(current_user):

    if not users[current_user][1]:
        return jsonify({'message': 'You are not allowed to perform this action!!'})

    data = request.get_json()

    new_movie = Movies(popularity=data['popularity'], director=data['director'], genre=data['genre'],
                       imdb_score=data['imdb_score'], movie_name=data['movie_name'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'New Movie added successfully.'})


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

        movie.movie_name = data['movie_name']
        movie.popularity = data['popularity']
        movie.director = data['director']
        movie.genre = data['genre']
        movie.imdb_score = data['imdb_score']

        db.session.commit()
        return jsonify({'message': 'Movie data updated successfully.'})


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


@app.route('/search', methods=['GET'])
@token_required
def search_movie(current_user):
    data = request.get_json()

    if not data:
        return jsonify({'message': "Please enter some data to search further."})

    elif 'id' in data.keys():
        movie = Movies.query.filter_by(id=data['id']).first()

        if not movie:
            return jsonify({'message': 'No Movie found for entered id!!'})

        else:
            movie_data = [{'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                           'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}]

            return jsonify({'Movie_data': movie_data})

    elif 'movie_name' in data.keys():
        movie = Movies.query.filter_by(movie_name=data['movie_name']).all()

        if not movie:
            return jsonify({'message': 'No Movie found for entered Name!!'})

        else:
            output = []

            for movie in movie:
                movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                              'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
                output.append(movie_data)

            return jsonify({'Movie_data': output})

    elif 'genre' in data.keys():
        movie = Movies.query.filter_by(genre=data['genre']).all()

        if not movie:
            return jsonify({'message': 'No Movie found for entered Genre!!'})

        else:
            output = []
            for movie in movie:
                movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                              'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
                output.append(movie_data)

            return jsonify({'Movie_data': output})

    elif 'popularity' in data.keys():
        movie = Movies.query.filter_by(popularity=data['popularity']).all()

        if not movie:
            return jsonify({'message': 'No Movie found for Popularity !!'})

        else:
            output = []
            for movie in movie:
                movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                              'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
                output.append(movie_data)

            return jsonify({'Movie_data': output})

    elif 'director' in data.keys():
        movie = Movies.query.filter_by(director=data['director']).all()

        if not movie:
            return jsonify({'message': 'No Movie found for entered Director!!'})

        else:
            output = []
            for movie in movie:
                movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                              'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
                output.append(movie_data)

            return jsonify({'Movie_data': output})

    elif 'imdb_score' in data.keys():
        movie = Movies.query.filter_by(imdb_score=data['imdb_score']).all()

        if not movie:
            return jsonify({'message': 'No Movie found for entered IMDB_Score!!'})

        else:
            output = []
            for movie in movie:
                movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                              'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
                output.append(movie_data)

            return jsonify({'Movie_data': output})

    else:
        return jsonify({'message': 'nothing'})


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
            'sub': user
            }
        return jsonify({'token': jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')})
    else:
        return jsonify({'message': 'You have entered wrong password!'})


if __name__ == '__main__':
    app.debug=True
    app.run()