import json
from flask import Blueprint, jsonify, request
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from PIL import Image
import cv2
import os
import io
import sys
import numpy as np
import base64
from datetime import datetime
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from inference_sdk import InferenceHTTPClient
from werkzeug.security import generate_password_hash, check_password_hash
import face_recognition
import cvzone
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
        d = list(collection.find({}))
        data = json.loads(json_util.dumps(d))
        print('data ' ,  data , type(data))
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