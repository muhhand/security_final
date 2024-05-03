from flask import Blueprint, jsonify, request
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
mongo = MongoClient(app.config['MONGO_URI'])
boolean_variable_collection = mongo.security.boolean_variable

mongo = PyMongo(app)

switch_post_bp = Blueprint('set_variable', __name__)





@switch_post_bp.route('/set_variable', methods=['POST'])
def set_variable():
    data = request.get_json()

    # Ensure the 'value' and 'userid' keys are present in the JSON data
    if 'value' not in data or 'userid' not in data:
        return jsonify({'error': 'Missing "value" or "userid" parameter in the request'}), 400

    new_value = data['value']
    userid = data['userid']
    isActive = data['isActive']

    # Update the variable in the MongoDB collection
    boolean_variable_collection.update_one({'userid': userid}, {'$set': {'value': new_value , "isActive" :isActive}}, upsert=True)

    return jsonify({'message': 'Variable updated successfully', 'variable': new_value, 'userid': userid , 'isActive':isActive})