__author__ = 'kacper'


class Path:
    send_path = "http://private-anon-4d6b494dc-bach.apiary-proxy.com/staff/~chaberb/apps/mail/msg"
    base_login = "http://private-anon-09c2921dd-bach.apiary-proxy.com/staff/~chaberb/apps/mail/login/"
    base_receiver = 'http://private-anon-c88ec10ab-bach.apiary-proxy.com/staff/~chaberb/apps/mail/user/'
    base_delete = "http://private-anon-4d6b494dc-bach.apiary-proxy.com/staff/~chaberb/apps/mail/msg/"

    @classmethod
    def login_path(cls, username):
        final_path = cls.base_login + username
        return final_path

    @classmethod
    def receive_path(cls, user):
        url = cls.base_receiver + user + '/messages'
        return url
    @classmethod
    def delete_path(cls, message_id):
        return cls.base_delete + message_id
