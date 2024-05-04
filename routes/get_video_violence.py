from flask import Blueprint, jsonify, request
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_pymongo import PyMongo



app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
mongo = MongoClient(app.config['MONGO_URI'])
videos_collection = mongo.security.videos
mongo = PyMongo(app)

get_video_bp = Blueprint('get_video', __name__)

def get_video():
    data = request.get_json()
   
    
    if 'userid' not in data:
        return jsonify({'error': 'Missing "userid" parameter in the request'}), 400

    userid = data['userid']  # Extract userid from the request
 
    # Check if the request has the 'video' file
    user_videos = videos_collection.find({'userid': userid})

    # Construct a list to store the retrieved video information
    videos = []
    for video in user_videos:
        videos.append({
            'title': video['title'],
            'date': video['date'],
            'hour': video['hour'],
            'video_filename': video['video_filename'],
            'video_url':video['video_url']                       # You can add more fields if needed
        })

    # Return the list of videos as a JSON response
    print(user_videos)
    return jsonify(videos), 200

    # Route for posting title, date, hour, and video file
@get_video_bp.route('/get_video', methods=['POST'])
def handle_get_video():
    return get_video()

