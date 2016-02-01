from .base import *
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from .. import gui


class LobbyScene(Scene):
    def __init__(self, engine):
        super(LobbyScene, self).__init__(engine)

        ratio = self.engine.getAspectRatio()

        width = ratio * 2 * 0.9
        height = 2 * 0.9

        header_height = 0.1 * height
        content_height = height - header_height

        self.main_frame = DirectFrame(
            scale=1, pos=(0, 0, 0), frameSize=(-width / 2, width / 2, - height / 2, height / 2),
            frameColor=(0.1, 0.1, 0.1, 1)
        )

        self.header_frame = DirectFrame(
            parent=self.main_frame,
            scale=1, frameSize=(0, width, 0, header_height), frameColor=(0.25, 0.2, 0.2, 1)
        )

        self.header_frame.alignTo(self.main_frame, gui.CT)

        self.content_frame = DirectFrame(
            parent=self.main_frame,
            scale=1, frameSize=(0, width, 0, content_height), frameColor=(0.2, 0.25, 0.2, 1)
        )

        self.content_frame.alignTo(self.main_frame, gui.CB)

        self.promo_frame = DirectFrame(
            parent=self.content_frame,
            scale=1, frameSize=(0, width / 4 * 3, 0, content_height / 3 * 2), frameColor=(0.2, 0.2, 0.25, 1)
        )

        self.promo_frame.alignTo(self.content_frame, gui.UL)

        self.games_frame = DirectFrame(
            parent=self.content_frame,
            scale=1, frameSize=(0, width / 4, 0, content_height / 3 * 2), frameColor=(0.25, 0.25, 0.2, 1)
        )

        self.games_frame.alignTo(self.content_frame, gui.UR)

        self.chat_frame = DirectFrame(
            parent=self.content_frame,
            scale=1, frameSize=(0, width, 0, content_height / 3), frameColor=(0.25, 0.2, 0.25, 1)
        )

        self.chat_frame.alignTo(self.content_frame, gui.LL)

        self.box_pivot = self.engine.render.attachNewNode('box-pivot')
        self.box_pivot.setScale(0.25, 0.25, 0.25)
        self.box_pivot.setPos(0, 0, 0)

        self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        self.box.reparentTo(self.box_pivot)
        self.box.setPos(-0.5, -0.5, -0.5)

        self.engine.taskMgr.add(self.rotate_box_task, 'rotate_box_task')

        # self.texture = self.engine.loader.loadTexture('./res/textures/pavement.jpg')
        # self.img = OnscreenImage(image=self.texture, pos=(0, 0, 0))
        # self.img.reparentTo(self.engine.aspect2d)

        # self.chat_frame = DirectFrame(scale=1, pos=(-ratio, 0, 1), frameSize=(0, ratio * 2, -0.1, 0), frameColor=(0, 0, 1, 1))
        # self.promo_frame = DirectFrame(scale=1, pos=(-ratio, 0, 0.9), frameSize=(0, ratio * 2 * 5.0/8.0, -1.4, 0), frameColor=(1, 0, 0, 1))
        # self.matches_frame = DirectFrame(scale=1, pos=(ratio, 0, 0.9), frameSize=(0, -ratio * 2 * 3.0/8.0, -1.4, 0), frameColor=(0, 1, 0, 1))
        # self.chat_frame = DirectFrame(scale=1, pos=(-ratio, 0, -1), frameSize=(0, ratio * 2, 0, 0.5), frameColor=(0, 0, 1, 1))
        # self.chat_scrolled_list = DirectScrolledList(
        #     scale=1, pos=(-1, 0, 1), frameSize=(0, ratio * 2, -0.5, 0), parent=self.chat_frame,
        #     # scrollBarWidth=0.04,
        #     # verticalScroll_relief=DirectGuiGlobals.FLAT,
        #     # verticalScroll_frameColor=(0.2, 0.2, 0.2, 1),
        #     incButton_relief=DirectGuiGlobals.FLAT,
        #     incButton_color=(0.5, 0.5, 0.5, 1),
        #     decButton_relief=DirectGuiGlobals.FLAT,
        #     decButton_color=(0.4, 0.4, 0.4, 1),
        #     # thumb_relief=DirectGuiGlobals.FLAT,
        #     # thumb_color = (0.4, 0.4, 0.4, 1),
        # )
        #
        # gui.alignTo(self.chat_scrolled_list, self.chat_frame, gui.LL)
        # # self.chat_scrolled_frame.reparentTo(self.chat_frame)
        # # self.chat_scrolled_frame.setPos((-1, 0, 1))

    def rotate_box_task(self, task):
        t = task.time * 50
        self.box_pivot.setHpr(t, t * 1.3, t * 1.7)
        # self.main_frame.setHpr(t, t * 1.3, t * 1.7)
        return Task.cont

    def destroy(self):
        self.engine.taskMgr.remove('rotate_box_task')
        super(LobbyScene, self).destroy()
