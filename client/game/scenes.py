from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Func
from direct.actor.Actor import Actor
from panda3d.core import *


class Scene(object):
    def __init__(self, engine):
        self.engine = engine

    def destroy(self):
        pass
        # print self.engine.render.getChildren()
        # for child in self.engine.render.getChildren():
        #     print 'Removing', child
        #     child.remove_node()


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
        self.plane.remove_node()
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


class MainScene(ClickableGroundScene):
    def __init__(self, engine):
        # PickableScene.__init__(self, engine)
        ClickableGroundScene.__init__(self, engine)

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

        if self.panda_walk:
            print 'STOP'
            self.panda_walk.finish()
        self.panda.loop('walk')

        self.panda_walk = Sequence(self.panda.posInterval(distance / move_speed, target, source), Func(lambda: self.panda.stop('walk')), name='move-panda')
        self.panda_walk.start()
        # Sequence(self.panda.hprInterval(0.5, self.panda))

    # def on_object_picked(self, obj):
    #     print 'Picked object:', obj

    def destroy(self):
        self.engine.ignore('mouse1')
        self.engine.ignore('space')
        self.panda.remove_node()
        super(ClickableGroundScene, self).destroy()


class SecondScene(PickableScene):
    def __init__(self, engine):
        super(SecondScene, self).__init__(engine)

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
        super(SecondScene, self).destroy()
