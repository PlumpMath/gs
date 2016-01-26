#!/usr/bin/env python2

from network import Channel
import socket
import time
# from ctypes import cdll
# import platform
import sys
import os

# sys.path.append(os.path.abspath())

# def init_steam():
#     arch, _ = platform.architecture()
#     if arch == '64bit':
#         i9c = cdll.LoadLibrary('./i9c_64.so')
#     else:
#         i9c = cdll.LoadLibrary('./i9c_32.so')
#
#     i9c.api_init()
#     i9c.api_request_ticket()
#     #time.sleep(3)
#     #i9c.api_get_ticket()
# #    steam_user = libsteam_api.SteamUser()
# #    libsteam_api.SteamAPI_ISteamUser_GetAuthSessionTicket()


def main2():
    # init_steam()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8881))

    channel = Channel(client, None)
    channel.send_packet(['test'])
    for packet in channel.read_packets():
        print packet

    # time.sleep(5)


from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import loadPrcFile
from math import sin, cos, pi
from random import random

loadPrcFile("config.prc")


def main():
    class Game(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)

            self.scene = self.loader.loadModel("usr/share/panda3d/models/environment.egg.pz")
            self.scene.reparentTo(self.render)

            self.scene.setScale(0.25, 0.25, 0.25)
            self.scene.setPos(-8, 42, 0)

            # Load animated model

            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
            self.taskMgr.add(self.spinPandaTask, "SpinPandaTask")
            self.pandaActor = Actor('usr/share/panda3d/models/panda-model.egg.pz', {'walk': 'usr/share/panda3d/models/panda-walk4.egg.pz'})

            self.pandaActor.reparentTo(self.render)
            self.pandaActor.setScale(0.005, 0.005, 0.005)
            self.pandaActor.loop('walk')

            self.walkAngle = 0

        def spinCameraTask(self, task):
            angleDegrees = task.time * 6.0
            angleRadians = angleDegrees * (pi / 180.0)
            self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
            self.camera.setHpr(angleDegrees, 0, 0)
            return Task.cont

        def spinPandaTask(self, task):
            # move = task.time
            # phase = int(move) % 4
            # print phase
            # pos = self.pandaActor.getPos()
            # if phase == 0:
            #     pos.y += 0.1
            # elif phase == 1:
            #     pos.x -= 0.1
            # elif phase == 2:
            #     pos.y -= 0.1
            # else:
            #     pos.x += 0.1
            # self.pandaActor.setPos(pos)
            # self.pandaActor.setHpr(360 / 4 * ((phase + 2) % 4), 0, 0)

            DIV = 5

            x = sin(task.time / DIV) * 5
            y = cos(task.time / DIV) * 5
            print task.time
            self.pandaActor.setPos(x, y, 0)
            self.pandaActor.setHpr(-task.time / 2 / pi * 360 / DIV + 90, 0, 0)

            # print task.time
            # self.pandaActor.setHpr(task.time * 100, 0, 0)
            # self.pandaActor.setPos(random() * 2 - 1, random() * 2 - 1, random() * 2 - 1)
            return Task.cont

    app = Game()
    app.run()

if __name__ == '__main__':
    main()
