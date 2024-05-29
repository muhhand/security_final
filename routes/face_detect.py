import json
from flask import Blueprint, jsonify, request
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId, json_util


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
#app.config['UPLOADED_PHOTOS_DEST'] = r'D:\scu\Backend1\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = MongoClient(app.config['MONGO_URI'])
detect_face = Blueprint('detect_face', __name__)
db = mongo.security
collection = db['students']


@detect_face.route('/get_faces', methods=['GET'])
def get_face_dsa():
    try:
        # Ensure request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Invalid input: No JSON data provided'}), 400
        
        # Get JSON data from the request
        data = request.get_json()
        if 'user_id' not in data:
            return jsonify({'error': 'Invalid input: user_id is required'}), 400
        
        user_id = data['user_id']
        
        # Retrieve documents matching the user_id from MongoDB
        documents = list(collection.find({"user_id": user_id}))
        
        if not documents:
            return jsonify({'error': 'No data found for the given user_id'}), 404
        
        # Convert MongoDB documents to JSON
        data = json.loads(json_util.dumps(documents))
        
        # Extract face encodings and image data
        known_face_encodings = [list(doc['image']) for doc in data if 'image' in doc]
        
        if not known_face_encodings:
            return jsonify({'error': 'No face encodings found for the given user_id'}), 404
        
        # Extract names (or IDs)
        names = [doc['_id']['$oid'] for doc in data if '_id' in doc]
        
        # Return the face encodings and names as JSON response
        return jsonify({'face_encoding': known_face_encodings, "data": names})
        
    except Exception as e:
        print('Error: ' + str(e))
        return jsonify({'error': str(e)}), 500

@detect_face.route('/get_data', methods=['POST'])
def get_data_ads():
    try:
        dat = request.get_json()
        if '_id' not in dat:
            return jsonify({'error': '_id field is required'}), 400
        
        data =  collection.find_one({'_id': ObjectId(dat['_id'])})
        if data is None:
            return jsonify({'error': 'No data found for the given _id'}), 404
        
        return jsonify({'name': data['name'] , 'code': data['code'],'grade': data['grade'],'faculty': data['faculty']})
        
    except Exception as e: 
        print('Error:', e)
        return jsonify({'error': 'Internal server error'}), 500