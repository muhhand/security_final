from flask import Blueprint, jsonify, request
from flask import Flask,  request, jsonify




import os

import numpy as np

from pymongo import MongoClient

from flask_pymongo import PyMongo

from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
mongo = MongoClient(app.config['MONGO_URI'])
users = mongo.security.users
mongo = PyMongo(app)

signup_bp = Blueprint('signup', __name__)


@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = {
        'username': username,
        'password': hashed_password
    }

    users.insert_one(new_user)

    return jsonify({'message': 'User created successfully'}), 201