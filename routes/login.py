from flask import Blueprint, jsonify, request
from flask import Flask,  request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash

app = Flask(__name__)





app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
mongo = MongoClient(app.config['MONGO_URI'])
users = mongo.security.users
mongo = PyMongo(app)

login_bp = Blueprint('login', __name__)

# Login route
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = users.find_one({'username': username})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Return user ID on successful login
    return jsonify({'user_id': str(user['_id']),'username': str(user['username']),'email': str(user['email']),'phone': str(user['phone'])}), 200


