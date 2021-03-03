from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Hello-guys-this-is-super-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://adminrahul:password@db4free.net:3306/fyndimdb"

db = SQLAlchemy(app)


# Table attribute connection class
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    imdb_score = db.Column(db.Float, nullable=False)
    movie_name = db.Column(db.String(80), nullable=False)


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to IMDB Task page.'})


@app.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movies.query.all()

    output = []

    for movie in movies:
        movie_data = {'Movie_id': movie.id, 'Movie_name': movie.movie_name, '99popularity': movie.popularity,
                      'Director': movie.director, 'Genre': movie.genre, 'IMDB_Score': movie.imdb_score}
        output.append(movie_data)

    return jsonify({'Movies': output})


@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()

    new_movie = Movies(popularity=data['popularity'], director=data['director'], genre=data['genre'],
                       imdb_score=data['imdb_score'], movie_name=data['movie_name'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'New Movie added successfully.'})


@app.route('/movies/<id>', methods=['PUT'])
def modify_movie_data(id):
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
def delete_movie(id):
    movie = Movies.query.filter_by(id=id).first()

    if not movie:
        return jsonify({'message': 'No Movie found for entered id!!'})
    else:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie is Deleted successfully.'})


@app.route('/search', methods=['GET'])
def search_movie():
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


if __name__ == '__main__':
    app.run(debug=True)
