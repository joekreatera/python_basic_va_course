from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import loadPrcFileData
from Player import Player
from InputManager import InputManager

loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")


class Starfox(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.scene = self.loader.loadModel("./models/world.egg")
        self.scene.reparentTo(self.render)

        base.cTrav = CollisionTraverser()
        self.collisionHandlerEvent = CollisionHandlerEvent()
        base.enableParticles()

        self.collisionHandlerEvent.addInPattern('into-%in')
        self.collisionHandlerEvent.addOutPattern('outof-%in')

        self.accept('into-collision_enemy' , self.crash )
        self.accept('into-collision_player' , self.crash )
        self.accept('into-collision_plane', self.crash )

        base.cTrav.addCollider( self.scene.find("player/collision**"), self.collisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("enemy1/collision**"), self.collisionHandlerEvent)
        base.cTrav.addCollider( self.scene.find("basePlane/collision**"), self.collisionHandlerEvent)

        self.player = self.scene.find("player")
        self.player.setPythonTag("ObjectController" , Player(self.player) )
        self.player.setPos(self.scene, 0,0,5)
        self.camera.setPos(self.render, 0,-50,10)
        self.taskMgr.add(self.update , "update")

        base.cTrav.showCollisions(self.render)

        InputManager.initWith(self, [
            InputManager.arrowUp,
            InputManager.arrowDown,
            InputManager.arrowRight,
            InputManager.arrowLeft,
            InputManager.keyS,
            InputManager.keyA,
            InputManager.space
            ] )

    def crash(self,evt):
        print(f"{evt}")

    def update(self, task):
        self.player.getPythonTag("ObjectController").update(self.scene, globalClock.getDt() )
        self.camera.lookAt(self.player)
        return Task.cont
fox = Starfox()
fox.run()
