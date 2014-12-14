# encoding: utf-8

import requests
from Paths import Path
from flask import session


def is_logged():
    if 'username' not in session:
        return False
    else:
        return True


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


def receive_messages(message_type):

    receive_url = Path.receive_path(str(session['user_id']))
    r = requests.get(receive_url)

    if r.status_code == requests.codes.ok:
        array_of_all_messages = r.json()
        messages_of_type = []
        for message in array_of_all_messages:
            if message['type'] == message_type:
                message['content'] = message['content'][0:20] + "..."
                message['title'] = message['title'][0:50]
                messages_of_type.append(message)
        return messages_of_type
    else:
        raise NameError('Could not fetch messages from server')


def set_read(message_id):
    url = Path.get_unread_path(message_id)
    requests.get(url)


def get_message(message_id):

    url = Path.get_message(message_id)
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        message = r.json()
        if message['to_user_id'] == session['user_id'] or message['from_user_id'] == session['user_id']:
            if message['unread'] == 1 and message['to_user_id'] == session['user_id']:
                set_read(message_id)
            return message
        else:
            raise NameError('Not allowed operation')
    else:
        return None


def get_username(user_id):
    url = Path.get_user_path(user_id)
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        user = r.json()
        return user['username']
    else:
        raise NameError('Error while loading user data')


#Niewydajny sposób pobierania user_id na podstawie username
#Konieczne jest pobranie całej listy userów i sprawdzanie
def get_user_id(username):

    url = Path.get_users_path()
    r = requests.get(url)

    print r

    if r.status_code == requests.codes.ok:
        users = r.json()
        for user in users:
            if user['username'] == username:
                return user['user_id']
        return -1
    else:
        return -2