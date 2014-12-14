# encoding: utf-8

from flask import Flask, session, request, redirect, url_for, render_template
from Login import valid_login
import requests
import os
import json
from Paths import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)
'''
option=0 - wyswietlamy liste wiadomosci
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            valid, user_id = valid_login(username, password)
            if valid:
                session['username'] = username
                session['user_id'] = user_id
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error_code=4)
        else:
            return render_template('login.html', error_code=3)
    else:
        return render_template('login.html')


@app.route('/')
def index():
    if 'username' in session:
        try:
            # TODO handle messages!
            messages = receive_messages('inbox')
            return render_template('user_account.html', username=session['username'], messages=messages, option=0)
        except NameError as detail:
            print 'Error: ', detail
            return render_template('user_account.html', error_code=2)
    else:
        return render_template('login.html')

@app.route('/send')
def send_messages():
    if 'username' in session:
        try:
            # TODO handle messages!
            messages = receive_messages('outbox')
            return render_template('user_account.html', username=session['username'], messages=messages, option=1)
        except NameError as detail:
            print 'Error: ', detail
            return render_template('user_account.html', error_code=2)
    else:
        return render_template('login.html')


def receive_messages(message_type):
    receive_url = Path.receive_path(str(session['user_id']))
    r = requests.get(receive_url)
    if r.status_code == requests.codes.ok:
        array_of_all_messages = r.json()
        messages_of_type = []
        for message in array_of_all_messages:
            if message['type'] == message_type:
                messages_of_type.append(message)
        return messages_of_type
    else:
        raise NameError('Could not fetch messages from server')

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('user_id')
    return redirect(url_for('index'))


@app.route('/new', methods=['POST', 'GET'])
def new_message():
    if request.method == 'POST':
        path = Path.send_path
        receiver = request.form['receiver'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        sender = session['user_id'].strip()
        dict = {'content': content, 'from_user_id': sender, 'to_user_id': receiver, 'title': title}
        headers = {"Content-Type": "application/json"}
        dict = json.dumps(dict)
        r = requests.post(path, data=dict, headers=headers)
        print 'jestem'
        if r.status_code == requests.codes.ok:
            return render_template('user_account.html', option=3, success=1)
        else:
            return render_template('user_account.html', option=3, success=0)
    else:
        return render_template('user_account.html', option=2)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)