from flask import Flask
from flask_socketio import SocketIO, emit




app = Flask(__name__)

socketio = SocketIO(app,debug=False, cors_allowed_origins='*',logger=True,
    engineio_logger=True)


@socketio.on('message')
def handle_message(data):
    try:
        emit('message', data, broadcast=True )
        print('server received message' ,data)
    except Exception as e:
        print('Error: ' + str(e))

@socketio.on('send to server')
def receive_frame_and_send_to_flutter(data):
    try:
        emit('receive from server' , data ,broadcast=True)
    except Exception as e:
        print('Error: ' + str(e))

@socketio.on('notification')
def handle_notification(data):
    try:
        emit('notification', data, broadcast=True )
        print('server received notification' ,data)
    except Exception as e:
        print('Error: ' + str(e))        

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


#port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    socketio.run(app, debug=False,allow_unsafe_werkzeug=True)
#web: gunicorn app:app
