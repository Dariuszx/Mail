# encoding: utf-8

from flask import Flask, session, request, redirect, url_for, render_template
from Tools import valid_login, receive_messages, get_message, get_username, get_user_id, is_logged
from datetime import timedelta
import requests
import os
import json
from Paths import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)


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
            messages = receive_messages('inbox')
            return render_template('user_account.html', username=session['username'], messages=messages, option=0)
        except NameError as detail:
            print 'Error: ', detail
            return render_template('user_account.html', error_code=2)
    else:
        return render_template('login.html')


@app.route('/send')
def send_messages(e=None):

    if 'username' in session:
        try:
            messages = receive_messages('outbox')
            return render_template('user_account.html', username=session['username'], messages=messages, option=1, e=e)
        except NameError as detail:
            print 'Error: ', detail
            return render_template('user_account.html', error_code=2)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():

    if session:
        session.pop('username')
        session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/new', methods=['GET', 'POST'])
def new_message():

    if not is_logged():
        return redirect(url_for('index'))

    if request.method == 'POST':
        path = Path.send_path

        if request.form['receiver'] and request.form['title'] and request.form['title']:
            receiver = get_user_id(request.form['receiver'].strip())

            if receiver < 0:
                return redirect(url_for('new_message'))

            title = request.form['title'].strip()
            content = request.form['content'].strip()
            sender = str(session['user_id'])
            print path, receiver, title, content, sender
            dict_json = {'content': content, 'from_user_id': sender, 'to_user_id': receiver, 'title': title}
            headers = {"Content-Type": "application/json"}
            dict_json = json.dumps(dict_json)
            r = requests.post(path, data=dict_json, headers=headers)
            if r.status_code == requests.codes.ok:
                return render_template('user_account.html', username=session['username'], option=3, success=1)
            else:
                return render_template('user_account.html', username=session['username'], option=3, success=0)
        else:
            return redirect(url_for('new'))
    else:
        return render_template('user_account.html', username=session['username'], option=2)


@app.route('/delete/<from_path>', methods=['POST'])
def delete_message(from_path):

    if not is_logged():
        return redirect(url_for('index'))

    messages = request.form.getlist('messages')

    for message_id in messages:
        path = Path.delete_path(message_id)
        r = requests.delete(path)
        if r.status_code == requests.codes.ok:
            continue

    if from_path == '0':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('send_messages'))


@app.route('/show/<message_id>')
def show_message(message_id):
    try:
        if not is_logged():
            return redirect(url_for('index'))

        message = get_message(message_id)
        if message is not None:
            message['from_username'] = get_username(str(message['from_user_id']))
            message['to_username'] = get_username(message['to_user_id'])
            return render_template('user_account.html', username=session['username'], option=4, message=message)
        else:
            raise NameError('Server response error')

    except NameError as detail:
        print 'Error', detail
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)