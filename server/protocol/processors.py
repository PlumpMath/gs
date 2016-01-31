import json


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
        self.client.channel.send_packet(['success', 'bar', {'x': 'y'}])
