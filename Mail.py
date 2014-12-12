from flask import Flask
from urllib2 import Request, urlopen
app = Flask(__name__)



@app.route('/login/<username>')
def login(username):
    values = "dupa"
    headers = {"Content-Type":"text/plain"}
    request = Request("http://requestb.in/1kos93j1", data=values, headers=headers)
    response_body = urlopen(request).read()
    return 'pupa'

@app.route('/')
def hello_world():
    return 'Hello World!'


def costam():
    return 'dupa'


if __name__ == '__main__':
    app.run()
