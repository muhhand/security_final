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
        data = request.get_json()
        user_id = data['user_id']
        d = list(collection.find({"user_id":user_id}))
        data = json.loads(json_util.dumps(d))
        known_face_encodings = []
        images = [doc['image'] for doc in data if 'image' in doc]
    
        for image in images:
            known_face_encodings.append(list(image))
        print(known_face_encodings[0])
        names = [doc['_id']['$oid'] for doc in data if '_id' in doc]

        return jsonify({'face_encoding': known_face_encodings, "data": names})
        
    except Exception as e: 
        print('Error' + str(e))
        return str(e)

@detect_face.route('/get_data', methods=['POST'])
def get_data_ads():
    try:
        dat = request.get_json()
        data =  collection.find_one({'_id':ObjectId(dat['_id'])})
        return jsonify({'name':data['name']})
        
    except Exception as e: 
        print('Error' + str(e))
        return str(e)