#!/usr/bin/env python2

from network import Channel
import socket
import time
#from ctypes import cdll
#import platform
import sys
import os

sys.path.append('.')

def init_steam():
    arch, _ = platform.architecture()
    if arch == '64bit':
        i9c = cdll.LoadLibrary('./i9c_64.so')
    else:
        i9c = cdll.LoadLibrary('./i9c_32.so')

    i9c.api_init()
    i9c.api_request_ticket()
    #time.sleep(3)
    #i9c.api_get_ticket()
#    steam_user = libsteam_api.SteamUser()
#    libsteam_api.SteamAPI_ISteamUser_GetAuthSessionTicket()


def main():
#    init_steam()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8881))

    channel = Channel(client, None)
    channel.send_packet(['test'])
    for packet in channel.read_packets():
        print packet

    time.sleep(5)

if __name__ == '__main__':
    main()
