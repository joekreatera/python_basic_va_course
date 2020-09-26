from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import TextureStage
from panda3d.core import loadPrcFileData
from direct.interval.IntervalGlobal import *

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

loadPrcFileData("" , "textures-auto-power-2 #f")
loadPrcFileData("" , "textures-power-2 none")
loadPrcFileData("" ,"textures-square none")

class FireShow(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.scene = self.loader.loadModel("./models/fire")
        self.scene.reparentTo(self.render)
        self.texture = self.loader.loadTexture("./models/dk-arcade.png")
        self.scene.setTexture(self.texture)

        self.scene.find("**/pCube1").removeNode()
        self.quad = self.scene.find("**/pPlane1")
        self.quad.setTransparency(1)
        self.taskMgr.add(self.update , "update")

        f1 = Func(self.frame,0)
        f2 = Func(self.frame,0.041354)
        f3 = Func(self.frame,0.0823839)
        f4 = Func(self.frame,0.126218)
        delay = Wait(0.2)

        self.seq =  Sequence(f1,delay,f2,delay,f3,delay,f4,delay)
        #self.seq.start()
        self.seq.loop()

    def frame(self, u):
        self.quad.setTexOffset(TextureStage.getDefault(), u ,0)

    def update(self, task):
        self.camera.setPos(self.render, 0,0,5)
        self.camera.lookAt(self.scene)
        return Task.cont
fire = FireShow()
fire.run()
