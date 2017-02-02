import time, threading
from flask import Flask, render_template, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room
from apis import skype

app = Flask(__name__, template_folder='./html')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

clients = {}

class User(object):
    def __init__(self, username):
        self.username = username
        self.accounts = {}
        self.sids = []

    def emit(self, event, data):
        for sid in self.sids:
            emit(event, data, room=sid)

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

# @app.route("/send", methods=['POST'])
# def sendMessage():
#     message = request.form['message']
#     sender = request.form['sender']
#     source = request.form['source']
#     recipient = request.form['recipient']
#     print 'Sending message to: ' + recipient + ': ' + message 
#     return jsonify({
#         'message': message,
#         'sender': sender,
#         'source': source,
#         'recipient': recipient
#     })

@app.route('/result',methods = ['POST', 'GET'])
def result():
    return render_template('index.html')
#   dump()
#   if request.method == 'POST':
#      return render_template("index.html",result = result)

@app.route("/about")
def about():
    return render_template('about.html')

# @socketio.on('requestMessages')
# def send_messages(data):
#     username = data['username']
#     password = data['password']
#     print username, password
#     messages_to_send = [{
#         'message': 'hello?',
#         'sender': 'Rachel Hong',
#         'source': 'skype',
#         'recipient': 'maxsun'
#     },
#     {
#         'message': 'you there?',
#         'sender': 'Andrew Wang',
#         'source': 'skype',
#         'recipient': 'maxsun'
#     },
#     {
#         'message': ':(',
#         'sender': 'Andrew Wang',
#         'source': 'skype',
#         'recipient': 'maxsun'
#     }]
#     for message in messages_to_send:
#         for s in clients[message['recipient']]:
#             s.emit('message', message)

def get_user_from_sid(sid):
    for key in clients:
        if sid in clients[key].sids:
            return clients[key]

@socketio.on('send')
def send_message(data):
    user = get_user_from_sid(request.sid)
    message = data['message']
    recipient = data['recipient']
    method = data['method']
    user.emit('message', {
                'message': message,
                'sender': user.username,
                'recipient': recipient,
                'source': method
            })
    user.accounts[method].send(recipient, message)
    # print username, message, recipient, method

@socketio.on('get')
def get_messages(data):
    user = get_user_from_sid(request.sid)
    # this is only for skype right now
    skype = user.accounts['skype']
    contacts = skype.contacts()
    contacts.remove('echo123')
    messages = []
    for contact in contacts:
        contact_messages = skype.get(contact)
        for cm in contact_messages:
            print cm
            messages.append({
                'message': cm,
                'sender': contact,
                'recipient': user.username,
                'source': 'skype'
            })
    for message in messages:
        for sid in user.sids:
            user.emit('message', message)

@socketio.on('connected')
def handle_message(data):
    username = data['username']
    password = data['password']
    print username, password
    print 'connected'
    if username in clients.keys():
        clients[username].sids.append(request.sid)
    else:
        newConn = User(username)
        newConn.sids.append(request.sid)
        newConn.accounts['skype'] = skype.login(None, 'gatherbois@gmail.com', 'Andrew_PAD_#_1')
        clients[username] = newConn

@socketio.on('disconnect') # NEED TO SET clients[key] to null instead of []
def disconnect():
    for key in clients.keys():
        if request.sid in clients[key].sids:
            clients[key].sids.remove(request.sid)
            if len(clients[key].sids) == 0:
                del clients[key]
                break

if __name__ == "__main__":
    socketio.run(app, debug=True)
