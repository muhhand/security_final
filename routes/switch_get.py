from flask import Blueprint, jsonify, request
from flask import Flask,  request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
mongo = MongoClient(app.config['MONGO_URI'])
boolean_variable_collection = mongo.security.boolean_variable

mongo = PyMongo(app)

switch_get_bp = Blueprint('get_variable', __name__)



@switch_get_bp.route('/get_variable', methods=['POST'])
def get_variable():
    data = request.get_json()

    # Ensure the 'value' and 'userid' keys are present in the JSON data
    if 'userid' not in data:
        return jsonify({'error': 'Missing "userid" parameter in the request'}), 400

    userid = data['userid']

    # Find the document with the provided userid
    variable_data = boolean_variable_collection.find_one({'userid': userid})

    # Check if document exists
    if variable_data:
        return jsonify({'variable': variable_data['value'] , 'isActive': variable_data['isActive']})
    else:
        return jsonify({'error': 'No variable found for the provided userid'}), 404