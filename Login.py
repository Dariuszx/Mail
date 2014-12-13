__author__ = 'dariusz'

import requests, json


# Function to validate
#

def valid_login(username, password):
    base_path = 'http://private-anon-09c2921dd-bach.apiary-proxy.com/staff/~chaberb/apps/mail/login/'
    val = password
    path = base_path + username
    headers = {"Content-Type": "text/plain"}
    r = requests.post(path, data=val, headers=headers)
    print r.status_code
    if r.status_code == requests.codes.ok:
        return True
    else:
        return False