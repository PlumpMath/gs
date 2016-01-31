import socket
import struct
import msgpack


class ChannelError(Exception):
    pass


class Channel(object):
    def __init__(self, conn=None, info=None):
        self.conn = conn
        self.info = info
        self.data = []

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('127.0.0.1', 8881))

    def send_packet(self, data):
        print ' >', data
        stream = msgpack.packb(data)
        self.conn.send(struct.pack('>H', len(stream) + 2) + stream)

    def read_packets(self):
        data = list(self.conn.recv(1024))
        if not data:
            raise ChannelError('Client closed connection.')
        self.data.extend(data)
        while True:
            if len(self.data) > 2:
                length = (ord(self.data[0]) << 8) + ord(self.data[1])
                if len(self.data) >= length:
                    buff = data[2:length]
                    self.data = data[length:]
                    try:
                        packet = msgpack.unpackb(''.join(buff), use_list=False)
                    except Exception as e:
                        raise ChannelError('Got bad packet: {}'.format(e.message))
                    print ' <', packet
                    yield packet
                else:
                    print 'Need {} more bytes'.format(length)
                    break
            else:
                break

    def close(self):
        try:
            self.conn.close()
        except:
            pass
