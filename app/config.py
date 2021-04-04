import os

uri = "mysql://{}:{}@{}/{}".format(
    os.environ.get('DB_USERNAME'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_SERVER_NAME'),
    os.environ.get('DB_NAME')
)


class Configuration:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = uri

