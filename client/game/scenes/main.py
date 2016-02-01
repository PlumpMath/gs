from .base import *


class MainScene(ClickableGroundScene, NotifiableScene):
    def __init__(self, engine):
        super(MainScene, self).__init__(engine)
        # Scene.__init__(self, engine)
        # ClickableGroundScene.__init__(self)
        # NotifiableScene.__init__(self)

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

        self.panda = Actor('usr/share/panda3d/models/panda-model.egg.pz',
                           {'walk': 'usr/share/panda3d/models/panda-walk4.egg.pz'})
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
            self.notify('Test notification {}'.format(NotifiableScene.last_id))
            self.last_show = task.time
            print 'SHOW'
        return Task.cont

    def follow_panda_task(self, task):
        self.engine.camera.lookAt(self.panda)
        return Task.cont

    def next_scene(self):
        self.engine.set_scene('cube.CubeScene')

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

        self.panda_walk = Sequence(self.panda.posInterval(distance / move_speed, target, source),
                                   Func(lambda: self.panda.stop('walk')), name='move-panda')
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
        super(MainScene, self).destroy()
        # ClickableGroundScene.destroy(self)
        # NotifiableScene.destroy(self)
        # Scene.destroy(self)
