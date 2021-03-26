from app import app
from flask_sqlalchemy import SQLAlchemy



if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')

else:
    app.config.from_object('config.DevelopmentConfig')

URI = "mysql://{}:{}@{}/{}".format(app.config['DB_USERNAME'],app.config['DB_PASSWORD'], app.config['DB_SERVER_NAME'], app.config['DB_NAME'])

# app.config['SQLALCHEMY_DATBASE_URI'] = f"mysql://{app.config['DB_USERNAME']}:{app.config['DB_PASSWORD']}@{app.config['DB_SERVER_NAME']}/{app.config['DB_NAME']}"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b8d20ec0f53090:46cce531@us-cdbr-east-03.cleardb.com/heroku_a9c1dd5c5ec85b3'

app.config['SQLALCHEMY_DATABASE_URI'] = URI


db = SQLAlchemy(app)