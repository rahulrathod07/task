import os

from app import app
from flask_sqlalchemy import SQLAlchemy


uri = "mysql://{}:{}@{}/{}".format(
    os.environ.get('DB_USERNAME'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_SERVER_NAME'),
    os.environ.get('DB_NAME')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
