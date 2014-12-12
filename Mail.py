from flask import Flask, render_template
import requests


app = Flask(__name__)


@app.route('/<values>')
def login(values):
    headers = {"Content-Type": "text/plain"}
    request = Request("http://private-anon-55e0abccd-bach.apiary-proxy.com/staff/~chaberb/apps/mail/login/"+values, data=values, headers=headers)

    response_body = urlopen(request).read()

    if not response_body:
        print "asddsa"

    return render_template('login.html', msg=response_body)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
