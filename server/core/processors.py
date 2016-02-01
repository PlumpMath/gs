import json
from .database import get_db


class AbstractProcessor(object):
    def __init__(self, client):
        self.client = client

    def destroy(self):
        self.client = None

    def process_packet(self, packet):
        raise NotImplementedError()


class AuthProcessor(AbstractProcessor):
    class State:
        UNAUTHORIZED = 0
        AUTHORIZED = 1

    def __init__(self, client):
        super(AuthProcessor, self).__init__(client)

        self.state = AuthProcessor.State.UNAUTHORIZED

    def process_packet(self, packet):
        try:
            action, login, password = packet
        except:
            return

        if action == 'auth':
            if login == 'anderson' and password == '12345678':
                self.client.channel.send_packet(['auth:result', 1])
            else:
                self.client.channel.send_packet(['auth:result', 0])
