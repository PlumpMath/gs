import sys
from time import time
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Func
from direct.actor.Actor import Actor
from panda3d.core import *
from panda3d.direct import CInterval
from direct.task.Task import Task
from direct.gui.DirectGui import *


class Scene(object):
    def __init__(self, engine):
        self.engine = engine

    def destroy(self):
        pass
        # print self.engine.render.getChildren()
        # for child in self.engine.render.getChildren():
        #     print 'Removing', child
        #     child.remove_node()

    def on_packet(self, packet):
        print 'UNHANDLED PACKET: {}'.format(packet)


class NotifiableScene(Scene):
    last_id = 0

    class Notification(object):
        def __init__(self, scene, font, message):
            NotifiableScene.last_id += 1
            self.id = NotifiableScene.last_id
            self.node = TextNode('Notification {}'.format(self.id))
            self.node.setText(message)
            self.node.setFont(font)
            self.node.setShadow(0, 0.05)
            self.node.setShadowColor(0, 0, 0, 1)
            self.nodePath = None
            self.nodePath = scene.engine.aspect2d.attachNewNode(self.node)
            # self.nodePath.setPos(-1, 0, -1)
            self.nodePath.setPos(-scene.engine.getAspectRatio() + 0.05, 0, 0)
            self.nodePath.setScale(0.04)
            self.valid_until = time() + 10

        def destroy(self):
            if self.nodePath:
                self.nodePath.remove_node()

    def __init__(self, engine):
        super(NotifiableScene, self).__init__(engine)
        self.notifications = []
        self.font = self.engine.loader.loadFont('res/fonts/Roboto-Regular-webfont.ttf')

    def notify(self, message):
        notification = NotifiableScene.Notification(self, self.font, message)
        self.notifications.append(notification)

        self.engine.taskMgr.add(self.update_notifications, 'update_notifications')

    def update_notifications(self, task):
        if len(self.notifications) > 10:
            for notification in self.notifications[:-10]:
                notification.destroy()
            self.notifications = self.notifications[-10:]
        y = 0
        for notification in self.notifications:
            if notification.valid_until < time():
                notification.destroy()
            else:
                y += 0.05
                notification.nodePath.setPos(-self.engine.getAspectRatio() + 0.05, 0, -y)
        return Task.cont

    def destroy(self):
        self.engine.taskMgr.remove('update_notifications')
        for notification in self.notifications:
            notification.destroy()

        super(NotifiableScene, self).destroy()


class PickableScene(Scene):
    def __init__(self, engine):
        super(PickableScene, self).__init__(engine)

        self.pickedObj = None

        self.engine.accept('mouse1', self.pick_object)

        self.picker = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.engine.camera.attachNewNode(self.pickerNode)

        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()

        self.pickerNode.addSolid(self.pickerRay)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))

        self.picker.addCollider(self.pickerNP, self.queue)

    def pick_object(self):
        mpos = self.engine.mouseWatcherNode.getMouse()
        self.pickedObj = None

        # self.camera.ls()

        self.pickedObj = None  # be sure to reset this
        self.pickerRay.setFromLens(self.engine.camNode, mpos.getX(), mpos.getY())
        self.picker.traverse(self.engine.render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            self.pickedObj = self.queue.getEntry(0).getIntoNodePath()

            parent = self.pickedObj.getParent()
            self.pickedObj = None

            while parent != self.engine.render:
                if parent.getTag('pickable') == 'true':
                    self.on_object_picked(parent)
                    self.pickedObj = parent
                    return parent
                else:
                    parent = parent.getParent()
        return None

    def on_object_picked(self, obj):
        raise NotImplementedError()

    def destroy(self):
        self.engine.ignore('mouse1')
        self.pickerNP.remove_node()
        super(PickableScene, self).destroy()

    def makePickable(self, newObj):
        newObj.setCollideMask(BitMask32.bit(1))
        newObj.setTag('pickable', 'true')


class ClickableGroundScene(Scene):
    def __init__(self, engine):
        super(ClickableGroundScene, self).__init__(engine)

        # self.camera.setPos(0, 60, 25)
        # self.camera.lookAt(0, 0, 0)
        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))
        self.intersection = None
        # self.model = self.engine.loader.loadModel("jack")
        # self.model.reparentTo(render)
        # cm = CardMaker("blah")
        # cm.setFrame(-100, 100, -100, 100)
        # self.engine.render.attachNewNode(cm.generate()).lookAt(0, 0, -1)

        self.engine.taskMgr.add(self.get_mouse_pos, "GetMousePos")

    def destroy(self):
        # self.plane.remove_node()
        self.engine.taskMgr.remove("GetMousePos")
        super(ClickableGroundScene, self).destroy()

    def get_ground_intersection(self):
        return self.intersection

    def get_mouse_pos(self, task):
        if self.engine.mouseWatcherNode.hasMouse():
            mpos = self.engine.mouseWatcherNode.getMouse()
            pos3d = Point3()
            nearPoint = Point3()
            farPoint = Point3()
            self.engine.camLens.extrude(mpos, nearPoint, farPoint)
            if self.plane.intersectsLine(pos3d,
                                         self.engine.render.getRelativePoint(self.engine.camera, nearPoint),
                                         self.engine.render.getRelativePoint(self.engine.camera, farPoint)):
                self.intersection = pos3d
                # print "Mouse ray intersects ground plane at ", pos3d
                # self.model.setPos(render, pos3d)
        return task.again
