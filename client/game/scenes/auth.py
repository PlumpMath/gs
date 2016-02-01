from .base import *
from direct.gui import DirectGuiGlobals


class AuthScene(Scene):
    def __init__(self, engine):
        super(AuthScene, self).__init__(engine)
        # Scene.__init__(self, engine)

        self.box_pivot = self.engine.render.attachNewNode('box-pivot')

        self.box = self.engine.loader.loadModel('usr/share/panda3d/models/box.egg.pz')
        self.box.reparentTo(self.box_pivot)
        self.box.setPos(-0.5, -0.5, -0.5)

        self.engine.camera.setPos(5, 5, 5)
        self.engine.camera.lookAt(self.box_pivot)

        self.font = self.engine.loader.loadFont('res/fonts/Neou-Bold.ttf')
        self.font2 = self.engine.loader.loadFont('res/fonts/Roboto-Regular-webfont.ttf')

        self.frame = DirectFrame(scale=1, pos=(0, 0, 0), frameSize=(-1, 1, -1, 1), frameColor=(0, 0, 0, 0.95))
        self.frame.reparentTo(self.engine.render2d)

        self.inputs = self.engine.aspect2d.attachNewNode('buttons')

        self.notification = TextNode('Login notification')
        self.notification.setText('Azaza!')
        self.notification.setFont(self.font2)
        self.notification.setAlign(TextNode.ACenter)
        self.notificationNP = self.engine.render.attachNewNode(self.notification)
        self.notificationNP.setPos(0, 0, 0.3)
        self.notificationNP.setScale(0.05)
        self.notificationNP.reparentTo(self.inputs)

        self.login = DirectEntry(
            entryFont=self.font2, pos=(0, 0, 0.2), frameColor=(1, 1, 1, 0.1), text_fg=(1, 1, 1, 1),
            scale=0.05, frameSize=(-7, 7, -1, 0.5), text_pos=(-6.8, -0.6),
            focus=True, command=self.focus_password,
        )
        self.login.reparentTo(self.inputs)

        self.password = DirectEntry(
            entryFont=self.font2, pos=(0, 0, 0.1), frameColor=(1, 1, 1, 0.1), text_fg=(1, 1, 1, 1), scale=0.05,
            frameSize=(-7, 7, -1, 0.5), text_pos=(-6.8, -0.6), obscured=True, command=self.do_start
        )
        self.password.reparentTo(self.inputs)

        # self.start = DirectButton(text=('Log in'), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.start = DirectButton(
            text=('Log in'.upper(),), scale=0.075, text_font=self.font, relief=DirectGuiGlobals.FLAT,
            text_fg=(1, 1, 1, 1), command=self.do_start,
            text_scale=(0.8, 0.8),
            frameSize=(-2, 2, -0.5, 1), frameColor=(1, 1, 1, 0.05)
        )
        self.start.setPos(-0.2, 0, -0.1)
        self.start.reparentTo(self.inputs)

        self.exit = DirectButton(
            text=('Exit'.upper(),), scale=0.075, text_font=self.font, relief=DirectGuiGlobals.FLAT,
            text_fg=(1, 1, 1, 1), command=self.do_quit,
            text_scale=(0.8, 0.8),
            frameSize=(-2, 2, -0.5, 1), frameColor=(1, 1, 1, 0.05)
        )
        self.exit.setPos(0.2, 0, -0.1)
        self.exit.reparentTo(self.inputs)

        self.engine.taskMgr.add(self.rotate_box_task, 'rotate_box_task')

        self.is_busy = False

        self.do_start('anderson', '12345678')

    def focus_password(self, *args):
        self.login['focus'] = 0
        self.password['focus'] = 1

    def do_start(self, *args):
        if self.is_busy:
            return

        if len(args) == 2:
            login, password = args
        else:
            login, password = self.login.get(), self.password.get()

        self.notification.setText('Attempting to log in...')
        self.notification.setTextColor(1, 1, 1, 0.74)
        self.engine.channel.send_packet(['auth', login, password])
        self.is_busy = True
        # self.engine.set_scene('main.MainScene')

    def on_packet(self, packet):
        if packet[0] == 'auth:result':
            self.is_busy = False
            if packet[1]:
                self.notification.setText('Welcome!')
                self.notification.setTextColor(0.3, 1, 0.3, 1)
                # self.engine.set_scene('lobby.LobbyScene')
                self.engine.set_scene('main.MainScene')
            else:
                self.notification.setText('Incorrect login or password.')
                self.notification.setTextColor(1, 0.3, 0.3, 1)
        else:
            super(AuthScene, self).on_packet(packet)
        # self.start['state'] = DirectGuiGlobals.DISABLED

    def do_quit(self):
        sys.exit(0)

    def rotate_box_task(self, task):
        t = task.time * 250
        self.box_pivot.setHpr(t, t * 1.3, t * 1.7)
        return Task.cont

    def destroy(self):
        self.box_pivot.remove_node()
        self.frame.remove_node()
        self.inputs.remove_node()
        self.engine.taskMgr.remove('rotate_box_task')
        super(AuthScene, self).destroy()
