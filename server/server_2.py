from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import random
import skype

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CURRENT_USERS = {}

class User(object):
    '''A class to represent a connected client'''
    def __init__(self, _id, sid):
        self._id = _id
        self.sid = sid
        self.services = {}

@socketio.on('connect')
def connect():
    '''Client connect'''
    sid = request.sid
    CURRENT_USERS[sid] = {}
    socketio.emit('num-users', len(CURRENT_USERS))
    join_room(sid)
    socketio.emit('id', sid, room=sid)
    print 'connect: %s' % str(sid)

@socketio.on('disconnect')
def disconnect():
    '''Client disconnect'''
    sid = request.sid
    leave_room(sid)
    del CURRENT_USERS[sid]
    socketio.emit('num-users', len(CURRENT_USERS))
    print 'disconnect: %s' % str(sid)

@socketio.on('acc-info')
def login_account(data):
    skype_object = skype.login(data['username'], data['password'])
    sid = request.sid
    CURRENT_USERS[sid]['skype'] = skype_object
    socketio.emit('contacts', skype_object.get_contacts(), room=sid)

@app.route("/")
def index():
    '''Display the home screen'''
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
