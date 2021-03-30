import jwt
import os

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash

app = Flask(__name__)

# from app import models
from app import views