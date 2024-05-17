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


forget_password_bp = Blueprint('forget_password', __name__)


@forget_password_bp.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.get_json()
    
    email = data.get('email')
    new_password = data.get('new_password')


    user = users.find_one({'email': email})

    if not user:
        return jsonify({'message': 'user not found'}), 401

    # Hash the new password
    new_password_hashed = generate_password_hash(new_password)

    # Update the user's password in the database
    users.update_one({'email': email}, {'$set': {'password': new_password_hashed}})

    return jsonify({'message': 'Password changed successfully'}), 200
