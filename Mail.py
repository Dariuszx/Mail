from flask import Flask, session, request, redirect, url_for, render_template
from Login import valid_login
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            if valid_login(username, password):
                session['username'] = login
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error_code=404)



@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)