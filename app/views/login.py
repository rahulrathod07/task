import jwt
import os

from app import app
from app.models import Users
from flask import jsonify, request
from werkzeug.security import check_password_hash


# Login user and token generation
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify. Please enter all the required details to login.'}), 401
    user = Users.query.filter_by(name=auth.username).first()
    if not user:
        return jsonify({'message': 'Username does not exist.'}), 401
    elif check_password_hash(user.password, auth.password):
        payload = {
            'user': user.serialized
        }
        return jsonify({'token': jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')})
    return jsonify({'message': 'You have entered wrong password.'}), 401

