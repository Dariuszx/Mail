from flask import Flask
import requests, time
app = Flask(__name__)



@app.route('/login/<username')
def login(username):

@app.route('/')
def hello_world():
    return 'Hello World!'


def costam():
    return 'dupa'


if __name__ == '__main__':
    app.run()
