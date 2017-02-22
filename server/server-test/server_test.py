from flask import Flask, request
app = Flask(__name__)

current_users = []

class User(object):
    '''A class to represent a connected client'''
    def __init__(self):
        self.services = {}

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
