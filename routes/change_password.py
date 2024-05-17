from flask import Blueprint, jsonify, request
from flask import Flask
from pymongo import MongoClient
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
mongo = MongoClient(app.config['MONGO_URI'])
users = mongo.security.users
mongo = PyMongo(app)


change_password_bp = Blueprint('change_password', __name__)


@change_password_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not email or not current_password or not new_password:
        return jsonify({'message': 'email, current password, and new password are required'}), 400

    user = users.find_one({'email': email})

    if not user or not check_password_hash(user['password'], current_password):
        return jsonify({'message': 'Current password is incorrect'}), 401

    # Hash the new password
    new_password_hashed = generate_password_hash(new_password)

    # Update the user's password in the database
    users.update_one({'email': email}, {'$set': {'password': new_password_hashed}})

    return jsonify({'message': 'Password changed successfully'}), 200
