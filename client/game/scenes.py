import sys
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


class NotifiableScene:
    last_id = 0

    class Notification(object):
        def __init__(self, scene, font, message):
            NotifiableScene.last_id += 1
            self.id = NotifiableScene.last_id
            self.node = TextNode('Notification {}'.format(self.id))
            self.node.setText(message)
            self.node.setFont(font)
            self.nodePath = None
            self.nodePath = scene.engine.aspect2d.attachNewNode(self.node)
            # self.nodePath.setPos(-1, 0, -1)
            self.nodePath.setPos(-scene.engine.getAspectRatio(), 0, 0)
            self.nodePath.setScale(0.04)

        def destroy(self):
            if self.nodePath:
                self.nodePath.remove_node()

    def __init__(self):
        # super(NotifiableScene, self).__init__(engine)
        self.notifications = []
        self.font = self.engine.loader.loadFont('res/fonts/Roboto-Regular-webfont.ttf')

    def notify(self, message):
        notification = NotifiableScene.Notification(self, self.font, message)
        self.notifications.append(notification)

    def destroy(self):
        for notification in self.notifications:
            notification.destroy()


class PickableScene:
    def __init__(self):
        # super(PickableScene, self).__init__(engine)

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
        # super(PickableScene, self).destroy()

    def makePickable(self, newObj):
        newObj.setCollideMask(BitMask32.bit(1))
        newObj.setTag('pickable', 'true')


class ClickableGroundScene:
    def __init__(self):
        # super(ClickableGroundScene, self).__init__(engine)

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
        # super(ClickableGroundScene, self).destroy()

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


class MenuScene(Scene):
    def __init__(self, engine):
        # super(MenuScene, self).__init__(engine)
        Scene.__init__(self, engine)

        self.box_pivot = self.engine.render.attachNewNode('box-pivot')

        self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        self.box.reparentTo(self.box_pivot)
        self.box.setPos(-0.5, -0.5, -0.5)

        self.engine.camera.setPos(5, 5, 5)
        self.engine.camera.lookAt(self.box_pivot)

        self.font = self.engine.loader.loadFont('res/fonts/Neou-Bold.ttf')

        self.frame = DirectFrame(scale=1, pos=(0, 0, 0), frameSize=(-1, 1, -1, 1), frameColor=(0, 0, 0, 0.95))
        self.frame.reparentTo(self.engine.render2d)

        self.buttons = self.engine.aspect2d.attachNewNode('buttons')

        # self.start = DirectButton(text=('Log in'), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.start = DirectButton(
            text=('Log in'.upper(),), scale=0.075, text_font=self.font, relief=None,
            text_fg=(1, 1, 1, 1), command=self.do_start
        )
        self.start.setPos(0, 0, 0.05)
        self.start.reparentTo(self.buttons)

        self.exit = DirectButton(
            text=('Exit'.upper(),), scale=0.075, text_font=self.font, relief=None,
            text_fg=(1, 1, 1, 1), command=self.do_quit
        )
        self.exit.setPos(0, 0, -0.05)
        self.exit.reparentTo(self.buttons)

        self.engine.taskMgr.add(self.rotate_box_task, 'rotate_box_task')

    def do_start(self):
        self.engine.set_scene(MainScene)

    def do_quit(self):
        sys.exit(0)

    def rotate_box_task(self, task):
        t = task.time * 250
        self.box_pivot.setHpr(t, t * 1.3, t * 1.7)
        return Task.cont

    def destroy(self):
        self.box_pivot.remove_node()
        self.frame.remove_node()
        self.buttons.remove_node()
        self.engine.taskMgr.remove('rotate_box_task')
        Scene.destroy(self)


class MainScene(Scene, ClickableGroundScene, NotifiableScene):
    def __init__(self, engine):
        # PickableScene.__init__(self, engine)
        Scene.__init__(self, engine)
        ClickableGroundScene.__init__(self)
        NotifiableScene.__init__(self)

        cm = CardMaker('ground')
        pavement = self.engine.loader.loadTexture('res/textures/pavement.jpg')
        self.ground = NodePath('Ground')
        cm.setFrame(-2, 2, -2, 2)

        for y in xrange(-2, 3):
            for x in xrange(-2, 3):
                part = NodePath(cm.generate())
                # self.ground.setTwoSided(True)
                part.setTexture(pavement)
                part.reparentTo(self.ground)
                part.setPos(x * 4, y * 4, 0)
                part.setHpr(0, -90, 0)
                # self.ground.attachNewNode(part)

        self.ground.reparentTo(self.engine.render)

        self.panda = Actor('usr/share/panda3d/models/panda-model.egg.pz', {'walk': 'usr/share/panda3d/models/panda-walk4.egg.pz'})
        self.panda.reparentTo(self.engine.render)
        self.panda.setScale(0.001, 0.001, 0.001)
        self.panda.setPlayRate(2.0, 'walk')

        self.panda_walk = None

    # self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        # self.box.reparentTo(self.engine.render)
        # self.makePickable(self.box)

        self.engine.camera.setPos(10, 10, 10)
        self.engine.camera.lookAt(self.panda)

        self.engine.accept('mouse1', self.on_world_clicked)

        self.engine.accept('space', self.next_scene)

        self.engine.taskMgr.add(self.follow_panda_task, 'follow_panda_task')
        self.engine.taskMgr.add(self.notification_task, 'notification_task')

        self.last_show = 0

    def notification_task(self, task):
        if self.last_show + 1 < task.time:
            self.notify('Test notification')
            self.last_show = task.time
            print 'SHOW'
        return Task.cont

    def follow_panda_task(self, task):
        self.engine.camera.lookAt(self.panda)
        return Task.cont

    def next_scene(self):
        self.engine.set_scene(SecondScene)

    def on_world_clicked(self):
        source = self.panda.getPos()
        target = self.get_ground_intersection()
        move_speed = 1.0
        distance = (target - source).length()
        self.panda.lookAt(target)
        self.panda.setHpr(self.panda.getHpr().x - 180, 0, 0)

        # source_hpr = self.panda.getHpr()
        # target_hpr = self.panda.getHpr()
        # target_hpr.x =

        if self.panda_walk and self.panda_walk.getState() == CInterval.SStarted:
            print 'STOP'
            self.panda_walk.clearToInitial()
            # self.panda_walk.finish()
        else:
            self.panda.loop('walk')

        self.panda_walk = Sequence(self.panda.posInterval(distance / move_speed, target, source), Func(lambda: self.panda.stop('walk')), name='move-panda')
        self.panda_walk.start()
        # Sequence(self.panda.hprInterval(0.5, self.panda))

    # def on_object_picked(self, obj):
    #     print 'Picked object:', obj

    def destroy(self):
        self.engine.taskMgr.remove('follow_panda_task')
        self.engine.taskMgr.remove('notification_task')
        self.engine.ignore('mouse1')
        self.engine.ignore('space')
        self.ground.remove_node()
        self.panda.remove_node()
        # super(ClickableGroundScene, self).destroy()
        ClickableGroundScene.destroy(self)
        NotifiableScene.destroy(self)
        Scene.destroy(self)


class SecondScene(Scene, PickableScene):
    def __init__(self, engine):
        Scene.__init__(self, engine)
        PickableScene.__init__(self)

        self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        self.box.reparentTo(self.engine.render)
        self.makePickable(self.box)

#        self.plant = self.engine.loader.loadModel('res/models/plant.egg.gz')
#        self.plant.reparentTo(self.engine.render)

#        self.plant.setPos(1, 1, 0)
#        self.plant.setScale(0.1, 0.1, 0.1)

        self.engine.accept('space', self.next_scene)

    def next_scene(self):
        self.engine.set_scene(MainScene)

    def on_object_picked(self, obj):
        print 'Picked', obj

        self.engine.set_scene(MainScene)

    def destroy(self):
        self.engine.ignore('space')
        self.box.remove_node()
#        self.plant.remove_node()
#         super(SecondScene, self).destroy()
        PickableScene.destroy(self)
        Scene.destroy(self)
