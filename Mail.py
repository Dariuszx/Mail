from flask import Flask, session, request, redirect, url_for, render_template
from Login import valid_login
import requests
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)


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
            return render_template('user_account.html', username=session['username'])
        except NameError as detail:
            print 'Error: ', detail
            return render_template('user_account.html', error_code=2)
    else:
        return render_template('login.html')


def receive_messages(message_type):
    base_url = 'http://private-anon-c88ec10ab-bach.apiary-proxy.com/staff/~chaberb/apps/mail/user/'
    base_url += str(session['user_id'])
    base_url += '/messages'
    r = requests.get(base_url)
    if r.status_code == requests.codes.ok:
        array_of_all_messages = r.json()
        messages_of_type = []
        for message in array_of_all_messages:
            if message['type'] == message_type:
                messages_of_type.append(message)
        return messages_of_type
    else:
        raise NameError('Could not fetch messages from server')

@app.route('/send')
def send_messages():
    return 'hello world'
@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('user_id')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)