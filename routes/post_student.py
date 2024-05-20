from flask import Blueprint, jsonify, request
from flask import Flask, request, jsonify
from pymongo import MongoClient
import face_recognition

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://mcmohand888:33119765@security.aw8optf.mongodb.net/security'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
mongo = MongoClient(app.config['MONGO_URI'])



upload_student_bp = Blueprint('upload_student', __name__)


@upload_student_bp.route('/post_data', methods=['POST'])
def post_data():
    try:
        # Get text data
        name_data = request.form.get('name')
        if not name_data:
            return jsonify({'error': 'name field is required'}), 400
        code_data = request.form.get('code')
        if not code_data:
            return jsonify({'error': 'code field is required'}), 400
        grade_data = request.form.get('grade')
        if not grade_data:
            return jsonify({'error': 'grade field is required'}), 400
        faculty_data = request.form.get('faculty')
        if not faculty_data:
            return jsonify({'error': 'faculty field is required'}), 400
        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({'error': 'faculty field is required'}), 400
        
        photo = request.files['photo']
        if not photo or not photo.filename:
            return jsonify({'error': 'Valid photo file is required'}), 400

        # Save photo to the 'uploads' directory with a secure filename
      
        image = face_recognition.load_image_file(photo)
        face_encoding = face_recognition.face_encodings(image)[0]
        # Convert base64 image data to bytes
       
        
        db = mongo.security
        collection = db['students']
        result = collection.insert_one({
            'user_id':user_id,
            'name': name_data, 
            'image': face_encoding.tolist(),
            'code': code_data, 
            'grade': grade_data, 
            'faculty': faculty_data
            })

        return jsonify({'message': 'Data successfully posted', 'id': str(result.inserted_id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    