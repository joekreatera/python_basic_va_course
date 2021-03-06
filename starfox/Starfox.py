from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, CollisionHandlerEvent
from panda3d.core import loadPrcFileData
from Player import Player
from DynamicEnemy import *
from InputManager import InputManager
from Path import Path
from Bullet import Bullet
from panda3d.core import Vec3

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

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

        #base.messenger.toggleVerbose()

        #self.collisionHandlerEvent.addInPattern('from-%in')
        self.collisionHandlerEvent.addInPattern('into-%in')
        self.collisionHandlerEvent.addOutPattern('outof-%in')


        self.player = self.scene.find("player")
        self.enemy   = self.scene.find("enemy1")
        self.player.setPythonTag("ObjectController" , Player(self.player, collisionMask = 0x4) )
        self.building_enemy = self.scene.find("building_enemy")

        #self.player.setPos(self.scene, 0,0,5)
        self.camera.setPos(self.render, 0,-50,100)
        self.taskMgr.add(self.update , "update")

        self.accept('into-collision_enemy' , self.crash )
        self.accept('into-collision_player' , self.crash )
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
        self.createStaticEnemy(self.building_enemy ,  200 , 850 , 0 )
        self.createStaticEnemy(self.building_enemy ,  -100 , 1000 , 0 )
        self.createDynamicEnemy(self.enemy,-80,500,20, -200,500, 20)

    def createDynamicEnemy(self, original, ox,oy,oz , tx=0,ty=0,tz=0):
        """
        de = DynamicEnemy( Vec3(ox,oy,oz), self.scene, original, self.player,
                base.cTrav,
                self.collisionHandlerEvent,
                vel=5,
                distanceToAttack = 80
            )
        de.setTargetPos( Vec3(tx,ty,tz) )
        """
        de = DynamicEnemy( Vec3(ox,oy,oz), self.scene, original, self.player,
                base.cTrav,
                self.collisionHandlerEvent,
                type = ENEMY_TYPE.CHASER,
                vel=35,
                distanceToAttack = 2000,
                collisionMask=0x3
            )

    def createStaticEnemy(self , original, x, y,z):
        be = original.copyTo(self.scene)
        be.setPos(self.scene, x ,y ,z )
        base.cTrav.addCollider(be.find("**collision**"), self.collisionHandlerEvent )
        be.find("**collision*").node().setIntoCollideMask(0x3)
        be.find("**collision*").node().setFromCollideMask(0x3)


    def crash(self,evt):
        #a = 2
        objectInto = evt.getIntoNodePath().node().getParent(0).getPythonTag("ObjectController")
        objectFrom = evt.getFromNodePath().node().getParent(0).getPythonTag("ObjectController")

        if( objectInto != None):
            objectInto.crash(objectFrom)

        if( objectFrom != None):
            objectFrom.crash(objectInto)

        print(f"{objectInto} {objectFrom}")

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
            b = Bullet(self.render, self.player.getPos(self.render) , self.enemy ,
                base.cTrav, self.collisionHandlerEvent, v, collisionMask=0x3)

        bullets = self.render.findAllMatches("bullet")

        for i in bullets:
            b = i.getPythonTag('ObjectController')
            b.update( globalClock.getDt())

        enemies = self.scene.findAllMatches("dynamicEnemy")

        for i in enemies:
            e = i.getPythonTag('ObjectController')
            s = e.update( globalClock.getDt(), self.rails)
            if( s ):
                dir = self.player.getPos(self.render) - i.getPos(self.render)
                dir.normalize()
                b = Bullet(self.render, i.getPos(self.render) ,
                                    self.enemy , base.cTrav,
                                    self.collisionHandlerEvent, dir ,
                                    collisionMask=0xC)



        return Task.cont
fox = Starfox()
fox.run()
