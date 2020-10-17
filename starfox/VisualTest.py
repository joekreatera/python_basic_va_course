from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import loadPrcFileData
from panda3d.core import DirectionalLight, AmbientLight, PointLight, Fog
from math import sin
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect

from panda3d.core import Vec3


from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode

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
        base.setBackgroundColor(0.1, 0.1, 0.1, 1)

        self.dirLight = DirectionalLight("dir light")
        self.dirLight.setShadowCaster(True, 512, 512)
        self.dirLight.color = (1,0,1,1)
        self.dirLightPath = self.render.attachNewNode(self.dirLight)
        self.dirLightPath.setHpr(45,-60,0)
        render.setLight(self.dirLightPath)
        self.angleTime = 0.0
        self.totalAngleTime = 10.0
        self.hAngle = 0


        self.ambientLight = AmbientLight("ambient")
        self.ambientLight.color = (0.1,0.1,0.1,1)
        self.ambLightPath = self.render.attachNewNode(self.ambientLight)
        render.setLight(self.ambLightPath)

        self.pointLight = PointLight("point")
        self.pointLight.color = (1,1,1,1)
        self.pointLightPath = self.render.attachNewNode(self.pointLight)
        self.pointLightPath.setPos(0,5,5)
        self.pointLight.setShadowCaster(True, 512, 512)
        self.render.setLight(self.pointLightPath)

        self.fog = Fog("fog")
        self.fog.setColor(.1,.1,.1)
        self.fog.setExpDensity(.3)
        self.fog.setLinearRange(150,200)
        self.fog.setLinearFallback(45,160,320)
        render.setFog(self.fog)
        self.render.setShaderAuto()


        self.p = self.render.attachNewNode("particles")
        base.enableParticles()
        p = ParticleEffect()
        p.loadConfig('./mysmoke.ptf')
        p.start(parent = self.p, renderParent = render)
        self.p.setPos(self.player, 0,0,2)

        self.font = loader.loadFont('./fonts/Magenta.ttf')
        self.sceneName = DirectLabel( text = "Starfox visual test",
            parent = self.aspect2d,
            scale = 0.07, pos = (-1.2,0,0.85),
            text_font = self.font, relief = None, text_fg = (1,1,1,1),
            textMayChange= True,
            text_align=TextNode.ALeft
            )

        self.foxy = OnscreenImage( image = './UI/fox-icon-png-8.png',
        pos = (1.2,9,0.85),
        scale = 0.1)
        self.foxy.setTransparency(True)

        self.controlsPanel = DirectDialog( frameSize = (-1.1,1.1,-0.9,-0.7),
            relief  = DGG.FLAT
        )

        btn = DirectButton( text = "Rotate",
            command = self.doRotate,
            image = './UI/fox-icon-png-8.png',
            pos = (-0.9,0,-0.8),
            parent = self.controlsPanel,
            scale = 0.07,
            relief = None
        )

        btn2 = DirectButton( text = "Anin Light",
            command = self.doLight,
            image = './UI/fox-icon-png-8.png',
            pos = (-0.7,0,-0.8),
            parent = self.controlsPanel,
            scale = 0.07,
            relief = None
        )

        self.camera.lookAt( self.player  )
        self.makeRotation = False
        self.rotateAngles = 0
        self.animLight = False

        filter = CommonFilters(base.win, base.cam)
        filter.setBloom(size="large", intensity=2)
        #filter.setAmbientOcclusion(strength = 5,  radius = 3)
        filter.setCartoonInk(separation=4)


    def doRotate(self):
        self.makeRotation = True
        return 0

    def doLight(self):
        self.animLight = True
        return 0

    def update(self,evt):
        ang = (self.angleTime/self.totalAngleTime)
        #self.camera.setPos(self.player, ang*100,ang*100,ang*100)

        self.player.setPos(self.render, 0,0,1)
        #self.camera.lookAt( Vec3(0,300,0) )

        #self.p.setPos(self.player, 0,0,0,)
        # self.dirLightPath.setHpr(ang*360.0 ,-60,0)
        if(  self.makeRotation  ):
            self.makeRotation = False
            self.rotateAngles = (self.rotateAngles + 90)%360
            self.player.setHpr(self.rotateAngles,0,0)
            self.sceneName["text"] = f"Starfox visual test ({self.rotateAngles})"

        self.camera.setPos(self.render, 10,10,10)
        self.camera.lookAt( self.player  )


        if( ang >= 1):
            self.angleTime = 0
        self.angleTime = self.angleTime + globalClock.getDt()
        self.dirLight.color = (ang,0,1,1)

        if self.animLight:
            self.pointLightPath.setPos(ang*10-5,ang*10-5,ang*5)

        return Task.cont
app = VisualTest()
app.run()
