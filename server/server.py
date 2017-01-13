import time, threading
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__, template_folder='./html')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

clients = []

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
        'sender': 'maxsun',
        'source': 'skype'
    },
    {
        'message': 'you there?',
        'sender': 'maxsun',
        'source': 'skype'
    },
    {
        'message': ':(',
        'sender': 'maxsun',
        'source': 'skype'
    }]
    for message in messages_to_send:
        socketio.emit('message', message)

@socketio.on('connected')
def handle_message(data):
    username = data['username']
    password = data['password']
    print username, password
    print 'connected'

if __name__ == "__main__":
    socketio.run(app, debug=True)
