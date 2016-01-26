#!/usr/bin/env python2

import gevent
from gevent import monkey
from gevent.server import StreamServer
from gevent.pool import Pool
import time
import socket
import select
from client import new_client

monkey.patch_all()

pool = Pool(1000)

server = StreamServer(('', 8881), new_client, spawn=pool)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print 'Terminating due to CTRL-BREAK.'
