from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import loadPrcFileData
from Player import Player
from DynamicEnemy import DynamicEnemy
from InputManager import InputManager
from Path import Path
from Bullet import Bullet
from panda3d.core import Vec3

loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")

"""
Trabajo:
Encontrar building_enemy
Duplicarlo en el escenario en las posiciones
50,20,0
-100,500,0
200,850,0
-100,1000,0

Agregar la colision a cTrav

Verificar que funcione la colision con la bala

"""

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
        self.building_enemy = self.scene.find("building_enemy")

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

        #self.createStaticEnemy(self.building_enemy ,  -100 ,500, 0 )
        #self.createStaticEnemy(self.building_enemy ,  200 , 850 , 0 )
        #self.createStaticEnemy(self.building_enemy ,  -100 , 1000 , 0 )
        self.createDynamicEnemy(self.enemy,-100,500,20)

    def createDynamicEnemy(self, original, x,y,z):
        de = DynamicEnemy( Vec3(x,y,z), self.scene, original, 0 )

    def createStaticEnemy(self , original, x, y,z):
        be = original.copyTo(self.scene)
        be.setPos(self.scene, x ,y ,z )
        base.cTrav.addCollider(be.find("building_enemy/collision**"), self.collisionHandlerEvent )

    def crash(self,evt):
        #a = 2
        print(f"{evt}")

    def update(self, task):
        extraX, extraZ = self.player.getPythonTag("ObjectController").update(self.rails, globalClock.getDt() )
        self.rails.setPos(self.scene,  Path.getXOfY(self.rails_y) , self.rails_y , 20 )
        #self.camera.lookAt(self.player)
        self.camera.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.rails.setHpr( Path.getHeading(self.rails_y) , 0, 0 )
        self.camera.setPos(self.rails , extraX, -10, extraZ)
        self.rails_y = self.rails_y + 20*globalClock.getDt()

        if self.player.getPythonTag("ObjectController").getShoot() :
            v = self.render.getRelativeVector(self.rails,Vec3(0,1,0))
            b = Bullet(self.render, self.player.getPos(self.render) , self.enemy , base.cTrav, self.collisionHandlerEvent, v)

        bullets = self.render.findAllMatches("bullet")

        for i in bullets:
            b = i.getPythonTag('ObjectController')
            b.update( globalClock.getDt())

        return Task.cont
fox = Starfox()
fox.run()
