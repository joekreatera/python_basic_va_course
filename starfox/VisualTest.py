from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import DirectionalLight, AmbientLight, PointLight
from math import sin
from panda3d.core import CardMaker

from panda3d.core import Vec3

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

class VisualTest(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.scene = loader.loadModel("models/world")
        self.player = self.scene.find("player");
        self.basePlane = self.scene.find("basePlane")
        self.player.reparentTo(self.render)
        self.basePlane.reparentTo(self.render)
        
        self.scene.remove_node()
        self.taskMgr.add(self.update, "update")

        self.camera.setPos(self.render, 0,-100,70)


        self.dirLight = DirectionalLight("dir light")
        self.dirLight.setShadowCaster(True, 512, 512)
        self.dirLight.color = (1,0,1,1)
        #self.dirLightPath = self.render.attachNewNode(self.dirLight)
        #self.dirLightPath.setHpr(45,-60,0)
        #render.setLight(self.dirLightPath)
        self.angleTime = 0.0
        self.totalAngleTime = 5.0
        self.hAngle = 0


        self.ambientLight = AmbientLight("ambient")
        self.ambientLight.color = (0,0,0,1)
        self.ambLightPath = self.render.attachNewNode(self.ambientLight)
        render.setLight(self.ambLightPath)

        self.pointLight = PointLight("point")
        self.pointLight.color = (1,1,1,1)
        self.pointLightPath = self.render.attachNewNode(self.pointLight)
        self.pointLightPath.setPos(0,5,5)
        self.render.setLight(self.pointLightPath)



    def update(self,evt):
        ang = (self.angleTime/self.totalAngleTime)
        self.camera.setPos(self.player, 10,10,10)
        #self.camera.lookAt( Vec3(0,300,0) )
        self.camera.lookAt( self.player  )

        # self.dirLightPath.setHpr(ang*360.0 ,-60,0)
        if( ang >= 1):
            self.angleTime = 0
        self.angleTime = self.angleTime + globalClock.getDt()
        self.dirLight.color = (ang,0,1,1)
        self.pointLightPath.setPos(0,5,ang*5)
        return Task.cont
app = VisualTest()
app.run()
