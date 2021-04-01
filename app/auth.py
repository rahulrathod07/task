import jwt
import os

from flask import jsonify, request
from functools import wraps


# Decorator for token decoding
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing.'})
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = data['user']
        except Exception as e:
            return jsonify({'message': 'Invalid Token. Login Again.'})
        return f(current_user, *args, **kwargs)
    return decorated


# Decorator for checking if user has admin privileges
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = args[0]
        if not current_user['admin']:
            return jsonify({'message': 'You are not allowed to perform this action.'}), 401
        return f(*args, **kwargs)
    return decorated

