import os

class config(object):
    DEBUG = False

    SECRET_KEY = os.urandom(24)

    DB_NAME = 'taskdb'
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_SERVER_NAME = 'localhost'

class ProductionConfig(config):

    DB_NAME = 'heroku_a9c1dd5c5ec85b3'
    DB_USERNAME = 'b8d20ec0f53090'
    DB_PASSWORD = '46cce531'
    DB_SERVER_NAME = 'us-cdbr-east-03.cleardb.com'

class DevelopmentConfig(config):
    DEBUG = True
    
