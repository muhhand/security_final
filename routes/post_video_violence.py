import os
from flask import Blueprint, jsonify, request, Flask
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError
from pymongo import MongoClient
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
videos_collection = mongo.db.videos

# Configure AWS S3
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
s3_bucket_name = 'securitybucket291'  # Replace with your S3 bucket name

post_video_bp = Blueprint('post_video', __name__)

def upload_to_s3(file, bucket_name, object_name=None):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        extra_args = {'ACL': 'public-read'}
        response = s3.upload_fileobj(file, bucket_name, object_name, ExtraArgs=extra_args)
    except ClientError as e:
        return None, e
    return response, None

def post_video():
    userid = request.form.get('userid')

    if 'video' not in request.files or not userid:
        return jsonify({'message': 'Invalid request: No video file or userid provided'}), 400

    video_file = request.files['video']
    video_filename = secure_filename(video_file.filename)

    if video_file:
        try:
            
            response, error = upload_to_s3(video_file, s3_bucket_name, video_filename)
            if error:
                return jsonify({'message': f'Failed to upload video to S3: {str(error)}'}), 500
        except Exception as e:
            return jsonify({'message': f'Failed to upload video to S3: {str(e)}'}), 500

        new_video = {
            'title': 'violence',
            'video_url': f'https://{s3_bucket_name}.s3.amazonaws.com/{video_filename}',
            'userid': userid,
            'date': video_filename.split('_')[0],
            'hour': video_filename.split('_')[1].split('.')[0],
            'video_filename': video_filename
        }

        try:
            videos_collection.insert_one(new_video)
            return jsonify({'message': 'Video posted successfully', 'video_url': new_video['video_url']}), 201
        except Exception as e:
            return jsonify({'message': f'Failed to save video metadata: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Failed to save the video file'}), 500

@post_video_bp.route('/post_video', methods=['POST'])
def handle_post_video():
    return post_video()

if __name__ == "__main__":
    app.run(debug=True)
