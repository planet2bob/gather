from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from apis import SkypeService
import eventlet
eventlet.monkey_patch()
async_mode = 'eventlet'
import time, threading
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room
from apis import SkypeService
import json

app = Flask(__name__, template_folder='./html')
app.config['SECRET_KEY'] = 'secretg!'
socketio = SocketIO(app)

CURRENT_USERS = {}

ping_check = []

class User(object):
    '''A class to represent a connected client'''
    def __init__(self, _id, sid):
        self._id = _id
        self.sid = sid
        self.services = {}

def ping_id(_id):
    socketio.emit('ping', room=_id)
    ping_check.append(_id)

@socketio.on('connect')
def connect():
    '''Client connect'''
    sid = request.sid
    CURRENT_USERS[sid] = {}
    socketio.emit('num_users', len(CURRENT_USERS))
    join_room(sid)
    socketio.emit('id', sid, room=sid)
    print 'connect: %s' % str(sid)

@socketio.on('disconnect')
def disconnect():
    '''Client disconnect using homemade DC event (the built in disconnect wasn't working)'''
    sid = request.sid
    leave_room(sid)
    del CURRENT_USERS[sid]
    socketio.emit('num_users', len(CURRENT_USERS))
    print 'disconnect: %s' % str(sid)

@socketio.on('acc_info')
def login_account(data):
    print data
    skype_object = SkypeService.login(data['username'], data['password'])
    sid = request.sid
    CURRENT_USERS[sid]['skype'] = skype_object
    socketio.emit('contacts', skype_object.get_contacts(), room=sid)

@app.route("/")
def index():
    '''Display the home screen'''
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/trylogin", methods=["POST",])
def verify():
    data = json.loads(request.data)
    password = data['password']
    username = data['username']
    print username, password
    return ''

if __name__ == '__main__':
    socketio.run(app, debug=True)
