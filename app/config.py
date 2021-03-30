from app import app, os
from flask_sqlalchemy import SQLAlchemy


URI = "mysql://{}:{}@{}/{}".format(
    os.environ.get('DB_USERNAME'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_SERVER_NAME'),
    os.environ.get('DB_NAME')
)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)