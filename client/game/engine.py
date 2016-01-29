from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec4
from scenes import MainScene
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import Sequence, Func, Wait, LerpFunc, Parallel
from direct.filter.CommonFilters import CommonFilters
from pandac.PandaModules import WindowProperties

loadPrcFile("config.prc")


class Engine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        props = WindowProperties()
        props.setTitle('Test')
        self.win.requestProperties(props)

        # self.render.setAntiAlias(AntialiasAttrib.MAuto)

        self.transitions = Transitions(self.loader)
        self.transitions.setFadeColor(0, 0, 0)

        self.filters = CommonFilters(self.win, self.cam)
        # self.filters.setCartoonInk()
        self.filters.setBlurSharpen(1)
        # self.filters.setVolumetricLighting(self.render)

        # self.buffer = self.win.makeTextureBuffer("Post-processing buffer", self.win.getXSize(), self.win.getXSize())
        # print self.buffer.getYSize()
        # self.texture = self.buffer.getTexture()
        # self.buffer.setSort(-100)
        #
        # self.originalCamera = self.camera
        # self.offScreenCamera = self.makeCamera(self.buffer)
        # self.camera = self.offScreenCamera
        #
        # self.img = OnscreenImage(image=self.texture, pos=(0, 0, 0.5))

        self.scene = None

        self.set_scene(MainScene)

    def set_scene(self, scene_class):
        # self.transitions.fadeOut(0.2)
        args = []

        if self.scene:
            args.append(Parallel(Func(self.fade_out), LerpFunc(self.blur_out, duration=0.2)))

        args.append(Func(self._set_scene, scene_class))
        args.append(Parallel(Func(self.fade_in), LerpFunc(self.blur_in, duration=0.4)))

        Sequence(*args).start()

    def blur_out(self, t):
        # index = int(t)
        # self.filters.delBlurSharpen()
        self.filters.setBlurSharpen(1 - t)
        self.filters.setBloom(intensity=t)

    def blur_in(self, t):
        # index = int(t)
        # self.filters.delBlurSharpen()
        self.filters.setBlurSharpen(t)
        self.filters.setBloom(intensity=-t)

    def fade_out(self):
        self.transitions.fadeOut(0.2)

    def fade_in(self):
        self.transitions.fadeIn(0.2)

    def _set_scene(self, scene_class):
        if self.scene:
            self.scene.destroy()
            del self.scene
        self.scene = scene_class(self)
        # self.transitions.fadeIn(0.2)

    def start(self):
        while True:
            self.taskMgr.step()
