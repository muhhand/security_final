from flask import Flask,send_from_directory
from flask_socketio import SocketIO, emit
import os



app = Flask(__name__)

socketio = SocketIO(app,debug=False, cors_allowed_origins='*',logger=True,
    engineio_logger=True)

from routes.face_detect import detect_face
from routes.signup import signup_bp
from routes.login import login_bp
from routes.post_video_violence import post_video_bp
from routes.swtich_post import switch_post_bp
from routes.switch_get import switch_get_bp
from routes.get_video_violence import get_video_bp

app.config['UPLOADED_VIDEOS_DEST'] = 'uploads/videos'
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOADED_VIDEOS_DEST'], filename)
 
app.register_blueprint(detect_face)
app.register_blueprint(signup_bp)#done
app.register_blueprint(login_bp)#done
app.register_blueprint(post_video_bp)
app.register_blueprint(switch_post_bp)
app.register_blueprint(switch_get_bp)
app.register_blueprint(get_video_bp)

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    socketio.run(app, debug=False,allow_unsafe_werkzeug=True,port=port)
#web: gunicorn app:app
