from flask import Blueprint, jsonify, request
from flask import Flask
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
    phone = data.get('phone')
    email = data.get('email')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if username, email, or phone already exists
    if users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    if users.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400
    if users.find_one({'phone': phone}):
        return jsonify({'message': 'Phone number already exists'}), 400

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = {
        'username': username,
        'password': hashed_password,
        'phone': phone,
        'email': email
    }

    users.insert_one(new_user)

    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.register_blueprint(signup_bp)
    app.run(debug=True)
