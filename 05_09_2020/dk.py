from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3
from panda3d.core import Vec4
from panda3d.core import OrthographicLens
from panda3d.core import loadPrcFileData


# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")

class DKApp(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.scene = self.loader.loadModel("models/DKSet1")
        self.scene.reparentTo(self.render)
        self.scene.setPos(0,0,0)
        self.jumping  = False
        self.jumpTime = 0
        # base.messenger.toggleVerbose()
        self.accept("raw-arrow_left" , self.pressLeft)
        self.accept("raw-arrow_left-up", self.releaseLeft)
        self.accept("raw-arrow_right" , self.pressRight)
        self.accept("raw-arrow_right-up", self.releaseRight)

        self.accept("raw-space" , self.pressSpace)
        self.accept("raw-space-up", self.releaseSpace)
        self.accept("raw-arrow_up" , self.pressUp)
        self.accept("raw-arrow_up-up", self.releaseUp)

        self.taskMgr.add(self.setup,"setup")
        self.taskMgr.add(self.update , "update")


        self.input=  {
            "up":False,
            "left":False,
            "right":False,
            "space":False
        }

    def pressLeft(self):
        self.input["left"] = True
    def releaseLeft(self):
        self.input["left"] = False
    def pressRight(self):
        self.input["right"] = True
    def releaseRight(self):
        self.input["right"] = False

    def pressSpace(self):
        self.input["space"] = True
    def releaseSpace(self):
        self.input["space"] = False
    def pressUp(self):
        self.input["up"] = True
    def releaseUp(self):
        self.input["up"] = False

    def getHorizontalAxis(self):
        if( self.input["left"] and self.input["right"]):
            return 0
        if( self.input["left"] ):
            return -1
        if( self.input["right"]):
            return 1

        return 0

    def setup(self, task):
        lens = OrthographicLens()
        lens.setFilmSize(25,20)
        base.camNode.setLens(lens)

        node = self.scene.find("root/camera1")
        node.remove()

        self.player = self.scene.find("root/mario")

        return Task.done

    def update(self,task):
        self.camera.setPos(0,35,0)
        self.camera.lookAt(self.scene)
        # print(f'{globalClock.getDt()}')
        jy = 0

        if self.jumping:
            self.jumpTime = self.jumpTime + globalClock.getDt()
            jy = 8*self.jumpTime  + 0.5*(-9)*self.jumpTime*self.jumpTime
            vy = 8 + (-9)*self.jumpTime
            if vy < 0 and abs(jy) < 0.2: # eventually jy substraction will change for the original y(aka Z) mario had
                self.jumpTime = 0
                self.jumping = False
                jy = 0
        else:
            if self.player.getZ() == 0 and  self.input["space"] :
                self.jumping = True
                self.jumpTime = 0.01


        self.player.setPos( self.player.getX()+self.getHorizontalAxis()*-.2 , 0, jy   )

        return Task.cont


dk = DKApp()
dk.run()
