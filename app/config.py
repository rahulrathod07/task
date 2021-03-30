from app import app, os
from flask_sqlalchemy import SQLAlchemy


URI = "mysql://{}:{}@{}/{}".format(
    app.config['DB_USERNAME'],
    app.config['DB_PASSWORD'],
    app.config['DB_SERVER_NAME'],
    app.config['DB_NAME']
)
# app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_DATABSE_URI'] =  URI
db = SQLAlchemy(app)