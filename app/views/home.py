from app import app
from flask import jsonify

# Home page
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to IMDB Task page.'})
