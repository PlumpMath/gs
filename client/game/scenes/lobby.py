from .base import *
from direct.gui.DirectGui import *


class LobbyScene(Scene):
    def __init__(self, engine):
        super(LobbyScene, self).__init__(engine)

        ratio = self.engine.getAspectRatio()

        self.main_frame = DirectFrame(
            scale=1, pos=(0, 0, 0), frameSize=(-ratio, ratio, -1, 1),
            frameColor=(0, 0, 0, 1)
        )

        ratio *= 0.8

        # self.texture = self.engine.loader.loadTexture('./res/textures/pavement.jpg')
        # self.img = OnscreenImage(image=self.texture, pos=(0, 0, 0))
        # self.img.reparentTo(self.engine.aspect2d)

        self.chat_frame = DirectFrame(scale=1, pos=(-ratio, 0, 1), frameSize=(0, ratio * 2, -0.1, 0), frameColor=(0, 0, 1, 1))
        self.promo_frame = DirectFrame(scale=1, pos=(-ratio, 0, 0.9), frameSize=(0, ratio * 2 * 5.0/8.0, -1.4, 0), frameColor=(1, 0, 0, 1))
        self.matches_frame = DirectFrame(scale=1, pos=(ratio, 0, 0.9), frameSize=(0, -ratio * 2 * 3.0/8.0, -1.4, 0), frameColor=(0, 1, 0, 1))
        self.chat_frame = DirectFrame(scale=1, pos=(-ratio, 0, -1), frameSize=(0, ratio * 2, 0, 0.5), frameColor=(0, 0, 1, 1))

    def destroy(self):
        super(LobbyScene, self).destroy()
