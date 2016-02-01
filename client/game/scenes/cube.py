from .base import *


class CubeScene(PickableScene):
    def __init__(self, engine):
        # Scene.__init__(self, engine)
        # PickableScene.__init__(self)

        super(CubeScene, self).__init__(engine)

        self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        self.box.reparentTo(self.engine.render)
        self.makePickable(self.box)

        #        self.plant = self.engine.loader.loadModel('res/models/plant.egg.gz')
        #        self.plant.reparentTo(self.engine.render)

        #        self.plant.setPos(1, 1, 0)
        #        self.plant.setScale(0.1, 0.1, 0.1)

        self.engine.accept('space', self.next_scene)

    def next_scene(self):
        self.engine.set_scene('main.MainScene')

    def on_object_picked(self, obj):
        print 'Picked', obj

        self.engine.set_scene('main.MainScene')

    def destroy(self):
        self.engine.ignore('space')
        self.box.remove_node()
        #        self.plant.remove_node()
        #         super(SecondScene, self).destroy()
        super(CubeScene, self).destroy()

# PickableScene.destroy(self)
#         Scene.destroy(self)
