from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():

    return render_template('login.html')


def is_logged():
    return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)