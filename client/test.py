#!/usr/bin/env python2

# from network import Channel
# import socket
# import time
# from ctypes import cdll
import platform
# import sys
# import os

# sys.path.append(os.path.abspath())

from game.engine import Engine
engine = Engine()
engine.start()

def init_steam():
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
    libsteam_api = cdll.LoadLibrary('old/libsteam_api.so')
    libsteam_api.SteamAPI_Init()
#     steam_
    # steam_user = libsteam_api.SteamUser()
# #    libsteam_api.SteamAPI_ISteamUser_GetAuthSessionTicket()


#init_steam()

#import time
#time.sleep(10)


def main2():
    init_steam()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8881))

    channel = Channel(client, None)
    channel.send_packet(['test'])
    for packet in channel.read_packets():
        print packet

    # time.sleep(5)


from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.core import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import Sequence
from math import sin, cos, pi
from random import random

loadPrcFile("config.prc")


def main():
    class CollisionMixin:
        def __init__(self):
            self.accept('mouse1', self.printMe)

            self.picker = CollisionTraverser()

            self.queue = CollisionHandlerQueue()

            self.pickerNode = CollisionNode('mouseRay')
            self.pickerNP = self.camera.attachNewNode(self.pickerNode)

            self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

            self.pickerRay = CollisionRay()

            self.pickerNode.addSolid(self.pickerRay)
            self.pickerNode.setFromCollideMask(BitMask32.bit(1))

            self.picker.addCollider(self.pickerNP, self.queue)

        # this function is meant to flag an object as being somthing we can pick
        def makePickable(self, newObj):
            newObj.setCollideMask(BitMask32.bit(1))
            newObj.setTag('pickable', 'true')

        # this function finds the closest object to the camera that has been hit by our ray
        def getObjectHit(self, mpos):  # mpos is the position of the mouse on the screen
            self.pickedObj = None

            # self.camera.ls()

            self.pickedObj = None  # be sure to reset this
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.render)
            if self.queue.getNumEntries() > 0:
                self.queue.sortEntries()
                self.pickedObj = self.queue.getEntry(0).getIntoNodePath()

                parent = self.pickedObj.getParent()
                self.pickedObj = None

                while parent != self.render:
                    if parent.getTag('pickable') == 'true':
                        self.pickedObj = parent
                        return parent
                    else:
                        parent = parent.getParent()
            return None

        def getPickedObj(self):
            return self.pickedObj

        def printMe(self):
            self.getObjectHit(base.mouseWatcherNode.getMouse())
            print self.pickedObj

    class Game(ShowBase, CollisionMixin):
        def __init__(self):
            ShowBase.__init__(self)
            CollisionMixin.__init__(self)

            base.disableMouse()

            self.accept('escape', sys.exit)

            # self.picker = Picker(self)

            # self.scene = self.loader.loadModel("usr/share/panda3d/models/environment.egg.pz")
            # self.scene.reparentTo(self.render)
            #
            # self.scene.setScale(0.25, 0.25, 0.25)
            # self.scene.setPos(-8, 42, 0)

            # self.picker.makePickable(self.scene)

            # Load animated model

            self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
            # self.taskMgr.add(self.spinPandaTask, "SpinPandaTask")
            # self.taskMgr.add(self.processLights, "ProcessLights")
            self.taskMgr.add(self.preProcess, "PreProcess")
            self.pandaActor = Actor('usr/share/panda3d/models/panda-model.egg.pz', {'walk': 'usr/share/panda3d/models/panda-walk4.egg.pz'})
            self.pandaActor.setCollideMask(BitMask32(1))
            self.makePickable(self.pandaActor)

            self.box = self.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
            self.box.reparentTo(self.render)
            self.box.setScale(2, 2, 2)
            self.box.setPos(0, 10, 0)
            self.makePickable(self.box)

            print self.camera

            # pandaPosInterval1 = self.pandaActor.posInterval(13,
            #                                                 Point3(0, -10, 0),
            #                                                 startPos=Point3(0, 10, 0))
            # pandaPosInterval2 = self.pandaActor.posInterval(13,
            #                                                 Point3(0, 10, 0),
            #                                                 startPos=Point3(0, -10, 0))
            # pandaHprInterval1 = self.pandaActor.hprInterval(3,
            #                                                 Point3(180, 0, 0),
            #                                                 startHpr=Point3(0, 0, 0))
            # pandaHprInterval2 = self.pandaActor.hprInterval(3,
            #                                                 Point3(0, 0, 0),
            #                                                 startHpr=Point3(180, 0, 0))
            #
            # # Create and play the sequence that coordinates the intervals.
            # self.pandaPace = Sequence(pandaPosInterval1,
            #                           pandaHprInterval1,
            #                           pandaPosInterval2,
            #                           pandaHprInterval2,
            #                           name="pandaPace")
            # self.pandaPace.loop()

            self.pandaActor.reparentTo(self.render)
            self.pandaActor.setScale(0.005, 0.005, 0.005)
            self.pandaActor.loop('walk')
            self.pandaActor.setPos(-3, 10, 0)

            self.walkAngle = 0

            # self.dlight = DirectionalLight('dlight 1')
            # self.dlnp = self.render.attachNewNode(self.dlight)
            #
            # self.dlnp.setPos(0, 0, 5)
            # self.dlnp.lookAt(self.pandaActor)

            self.plight = PointLight('plight 1')
            self.plnp = self.render.attachNewNode(self.plight)
            self.plnp.setColor(VBase4(1, 0.2, 0.2, 1))
            self.plnp.setPos(0, 0, 5)
            self.plight.setShadowCaster(True, 512, 512)
            # self.plight.setAttenuation((0, 0, 1))

            self.render.setShaderAuto()
            self.render.setLight(self.plnp)

            # self.camera.setPos(0, -10, 0)

        def preProcess(self, task):
            # print self.camera
            # self.picker.update()
            return Task.cont

        def spinCameraTask(self, task):
            # self.camera.setPos(20, 20, 20)
            self.camera.setPos(0, -task.time, 0)
            # self.camera.lookAt(self.pandaActor)
            # angleDegrees = task.time * 6.0
            # angleRadians = angleDegrees * (pi / 180.0)
            # self.camera.setPos(25 * sin(angleRadians), -25.0 * cos(angleRadians), (sin(task.time / 2) + 1) / 2 * 5 + 15)
            # self.camera.setHpr(angleDegrees, 0, 0)
            # self.camera.lookAt(self.pandaActor)
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
            self.pandaActor.setPos(x, y, 0)
            self.pandaActor.setHpr(-task.time / 2 / pi * 360 / DIV + 90, 0, 0)

            # print task.time
            # self.pandaActor.setHpr(task.time * 100, 0, 0)
            # self.pandaActor.setPos(random() * 2 - 1, random() * 2 - 1, random() * 2 - 1)
            return Task.cont

        def processLights(self, task):
            angleDegrees = -task.time * 360.0
            angleRadians = angleDegrees * (pi / 180.0)
            self.plnp.setPos(5 * sin(angleRadians), -5 * cos(angleRadians), 10)
            self.plnp.setHpr(angleDegrees, 0, 0)
            self.plnp.lookAt(self.pandaActor)
            return Task.cont

    app = Game()
    app.run()

if __name__ == '__main__':
    main()
