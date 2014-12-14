__author__ = 'dariusz'

import requests
from Paths import Path


def valid_login(username, password):
    val = password
    path = Path.login_path(username)
    headers = {"Content-Type": "text/plain"}
    r = requests.post(path, data=val, headers=headers)
    if r.status_code == requests.codes.ok:
        dict = r.json()
        user_id = dict['user_id']
        return True, user_id
    else:
        return False, None