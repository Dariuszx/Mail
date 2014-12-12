from flask import Flask
import requests
app = Flask(__name__)


@app.route('/login/<username>')
def login(username):
    base_path = 'http://private-anon-09c2921dd-bach.apiary-proxy.com/staff/~chaberb/apps/mail/login/'
    val = username
    path = base_path + username
    headers = {"Content-Type": "text/plain"}
    r = requests.post(path, data=val, headers=headers)
    return r.content


@app.route('/')
def hello_world():
    return 'Hello World!'


def costam():
    return 'dupa'
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)