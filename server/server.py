import time, threading
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__, template_folder='./html')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

clients = {}

class Socket:
    def __init__(self, sid):
        self.sid = sid
        self.connected = True

    # Emits data to a socket's unique room
    def emit(self, event, data):
        emit(event, data, room=self.sid)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/tryLogin", methods=['POST'])
def checkLogin():
    email = request.json['email']
    pwd = request.json['pwd']
    return pwd

@app.route("/send", methods=['POST'])
def sendMessage():
    message = request.form['message']
    sender = request.form['sender']
    source = request.form['source']
    recipient = request.form['recipient']
    return jsonify({
        'message': message,
        'sender': sender,
        'source': source,
        'recipient': recipient
    })

@app.route('/result',methods = ['POST', 'GET'])
def result():
    return render_template('index.html')
#   dump()
#   if request.method == 'POST':
#      return render_template("index.html",result = result)

@app.route("/about")
def about():
    return render_template('about.html')

@socketio.on('requestMessages')
def send_messages(data):
    username = data['username']
    password = data['password']
    print username, password
    # RETRIEVE UNSENT MESSAGES FROM DB USING USERNAME + PASSWORD
    messages_to_send = [{
        'message': 'hello?',
        'sender': 'Rachel Hong',
        'source': 'skype',
        'recipient': 'maxsun'
    },
    {
        'message': 'you there?',
        'sender': 'Andrew Wang',
        'source': 'skype',
        'recipient': 'maxsun'
    },
    {
        'message': ':(',
        'sender': 'Andrew Wang',
        'source': 'skype',
        'recipient': 'maxsun'
    }]
    for message in messages_to_send:
        for s in clients[message['recipient']]:
            s.emit('message', message)

@socketio.on('connected')
def handle_message(data):
    username = data['username']
    password = data['password']
    print username, password
    print 'connected'
    if username in clients.keys():
        clients[username].append(Socket(request.sid))
    else:
        clients[username] = [Socket(request.sid)]

@socketio.on('disconnect') # NEED TO SET clients[key] to null instead of []
def disconnect():
    for key in clients.keys():
        for s in clients[key]:
            if s.sid == request.sid:
                clients[key].remove(s)
                break

if __name__ == "__main__":
    socketio.run(app, debug=True)
