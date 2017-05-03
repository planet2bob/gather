from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from apis import SkypeService
import eventlet
eventlet.monkey_patch()
async_mode = 'eventlet'
import time, threading
from flask import Flask, render_template, request, session, jsonify, redirect
from flask_socketio import SocketIO, emit, join_room
from apis import SkypeService
import json

import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

session=botocore.session.get_session()
AWS_SECRET_KEY = session.get_credentials().secret_key
AWS_ACCESS_KEY = session.get_credentials().access_key

session = botocore.session.get_session()
dynamodb = boto3.resource('dynamodb', 
                            aws_access_key_id=AWS_ACCESS_KEY, 
                            aws_secret_access_key=AWS_SECRET_KEY, 
                            region_name='us-west-2')

app = Flask(__name__, template_folder='./html')
app.config['SECRET_KEY'] = 'secretg!'
socketio = SocketIO(app)

CURRENT_USERS = {}

ping_check = []

class User(object):
    '''A class to represent a connected client'''
    def __init__(self, sid):
        self.sid = sid
        self.services = {}
        self.logged_in = False

def ping_id(_id):
    socketio.emit('ping', room=_id)
    ping_check.append(_id)

TABLE = dynamodb.Table('gather')

def put_item(item):
    if 'username' not in item.keys():
        raise ValueError("put_item's item must have key 'username'")
    TABLE.put_item(
        Item=item
    )

def update_item(item_key, keys,):
    key_options = 'abcdefghijklmnopqrstuvwxyz'
    attr_values = {}
    update_expression = 'set '
    for i, key in enumerate(keys):
        update_expression += key + ' = :' + key_options[i] + ', '
        attr_values[':' + key_options[i]] = keys[key]
    update_expression = update_expression[:-2]
    TABLE.update_item(
        Key={'username': item_key},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=attr_values
    )

def get_item(item_key):
    result = TABLE.get_item(Key={'username':item_key})
    try:
        return result['Item']
    except KeyError:
        print 'Username "%s" does not exist in DB!' % item_key
        return None

def remove_item(item_key):
    result = TABLE.delete_item(Key={'username':item_key})
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return status_code

def create_account(username, password_hash):
    account_object = {
        'username': username,
        'password': password_hash,
        'services': []
    }
    put_item(account_object)

def try_to_login(username, password_hash):
    acc = get_item(username)
    if acc:
        return acc['password'] == password_hash
    return False

def add_service_to_account(username, service_obj):
    account = get_item(username)
    new_services = account['services'] + [service_obj]
    update_item(username, {
        'services': new_services
    })

@socketio.on('connect')
def connect():
    '''Client connect'''
    sid = request.sid
    CURRENT_USERS[sid] = User(sid)
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

@socketio.on("login")
def verify(data):
    password = data['password']
    username = data['username']
    print username, password
    if try_to_login(username, password):
        print 'Redirect!'
        # print CURRENT_USERS[request.sid]
        CURRENT_USERS[request.sid].logged_in = True
    socketio.emit('refresh', room=request.sid)

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

if __name__ == '__main__':
    socketio.run(app, debug=True)
