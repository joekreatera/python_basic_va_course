from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import loadPrcFileData
from Player import Player
from InputManager import InputManager
from Path import Path
from Bullet import Bullet

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")


class Starfox(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        self.scene.reparentTo(self.render)

        base.cTrav = CollisionTraverser()
        self.collisionHandlerEvent = CollisionHandlerEvent()
        base.enableParticles()

        base.messenger.toggleVerbose()

        #self.collisionHandlerEvent.addInPattern('from-%in')
        self.collisionHandlerEvent.addInPattern('into-%in')
        self.collisionHandlerEvent.addOutPattern('outof-%in')


        self.player = self.scene.find("player")
        self.enemy   = self.scene.find("enemy1")
        self.player.setPythonTag("ObjectController" , Player(self.player) )
        #self.player.setPos(self.scene, 0,0,5)
        self.camera.setPos(self.render, 0,-50,100)
        self.taskMgr.add(self.update , "update")

        self.accept('into-collision_enemy' , self.crash )
        self.accept('into-collision_player' , self.player.getPythonTag("ObjectController").collisionEnter )
        self.accept('into-collision_plane', self.crash )

        base.cTrav.addCollider( self.scene.find("player/collision**"), self.collisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("enemy1/collision**"), self.collisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("basePlane/collision**"), self.collisionHandlerEvent)

        #base.cTrav.showCollisions(self.render)

        InputManager.initWith(self, [
            InputManager.arrowUp,
            InputManager.arrowDown,
            InputManager.arrowRight,
            InputManager.arrowLeft,
            InputManager.keyS,
            InputManager.keyA,
            InputManager.space,
            InputManager.keyX,
            InputManager.keyV
            ] )

        self.rails = self.scene.attachNewNode("rails")
        self.rails.setPos(self.scene, 0,0,0)
        self.rails_y = 0
        self.player.reparentTo(self.rails)

        self.player.setPos(self.rails,0,20,0)

    def crash(self,evt):
        a = 2
        #print(f"{evt}")

    def update(self, task):
        extraX, extraZ = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y , 20 )
        #self.camera.lookAt(self.player)
        self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.camera.setPos(self.rails , extraX, -10, extraZ)
        self.rails_y = self.rails_y + 20*globalClock.getDt()

        if InputManager.isInputDown(InputManager.space):
            b = Bullet(self.render, self.player.getPos(self.render) , self.enemy , base.cTrav, self.collisionHandlerEvent)

        bullets = self.render.findAllMatches("bullet")

        for i in bullets:
            b = i.getPythonTag('ObjectController')
            b.update( globalClock.getDt())
            
        return Task.cont
fox = Starfox()
fox.run()
