from app import db
from werkzeug.security import generate_password_hash


# Movie info table
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    director = db.Column(db.String(80), nullable=False)
    popularity = db.Column(db.Integer(), nullable=False)
    imdb_score = db.Column(db.Float(), nullable=False)
    genres = db.relationship(
        "Genres",
        secondary="movie_genres",
        viewonly=True
    )

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'genre': [x.name for x in self.genres],
            '99popularity': self.popularity,
            'imdb_score': self.imdb_score
        }


class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class MovieGenres(db.Model):
    __tablename__ = 'movie_genres'
    id = db.Column(db.Integer(), primary_key=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.id', ondelete='CASCADE'))
    genre_id = db.Column(db.Integer(), db.ForeignKey('genres.id', ondelete='CASCADE'))


# Users info table
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(500))
    admin = db.Column(db.Boolean)

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'admin': self.admin
        }


# Initialize databases. create tables and users for testing.
def initialize_db():
    db.create_all()
    new_admin = Users(
        name='admin',
        password=generate_password_hash('admin', method='sha256'),
        admin=True
    )
    new_user = Users(
        name='user',
        password=generate_password_hash('user', method='sha256'),
        admin=False
    )
    db.session.add(new_admin)
    db.session.add(new_user)
    db.session.commit()