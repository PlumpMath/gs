from common.network import Channel, ChannelError
from core.processors import AuthProcessor


class Client(object):
    connections = []
    last_id = 0
    matches = []

    def __init__(self, conn, info):
        self.id = None

        self.channel = Channel(conn, info)
        self.processor = AuthProcessor(self)

        self.data = {}

        Client.add_client(self)

        self.loop()

    def loop(self):
        while True:
            try:
                for packet in self.channel.read_packets():
                    self.processor.process_packet(packet)
            except ChannelError as e:
                return Client.remove_client(self, e.message)

    def set_processor(self, processor):
        self.processor.destroy()
        self.processor = processor

    @classmethod
    def new_client(cls, conn, info):
        Client(conn, info)

    @classmethod
    def add_client(cls, client):
        Client.last_id += 1
        client.id = Client.last_id
        cls.connections.append(client)
        print 'New client {}'.format(client)

    @classmethod
    def remove_client(cls, client, reason):
        client.set_processor(None)
        client.channel.close()
        cls.connections.remove(client)
        print '{} disconnected. Reason: {}'.format(client, reason)

    def __str__(self):
        return '<Client {}>'.format(self.id)

def new_client(conn, info):
    return Client.new_client(conn, info)
