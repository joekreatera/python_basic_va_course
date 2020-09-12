from math import pi,cos,sin
from random import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor

from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import OrthographicLens
from panda3d.core import NodePath
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce,PhysicsCollisionHandler
from panda3d.core import AmbientLight
from panda3d.core import Vec4, LVector3
from panda3d.core import CollisionBox, CollisionSphere
from panda3d.core import CollisionRay, CollisionSegment
from panda3d.core import CollisionNode, BitMask32
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerEvent
from panda3d.core import DirectionalLight
from panda3d.core import loadPrcFileData
from direct.gui.DirectGui import *

loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")

class DKGame(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.loadScenery()
        self.mario = None
        #base.messenger.toggleVerbose()
        self.taskMgr.add(self.setup, "setup")
        self.taskMgr.add(self.update, "update")

        self.accept("raw-arrow_right" , self.pressRight)
        self.accept("raw-arrow_right-up" , self.stopRight)
        self.accept("raw-arrow_left" , self.pressLeft)
        self.accept("raw-arrow_left-up" , self.stopLeft)

        self.accept("raw-arrow_up" , self.pressUp)
        self.accept("raw-arrow_up-up" , self.stopUp)

        self.accept("raw-space" , self.pressSpace)
        self.accept("raw-space-up" , self.stopSpace)


        self.canClimb = False
        self.isClimbing = False
        #NUEVA!
        self.isGrounded = True
        self.canJump = True
        self.jumpTime = 0
        self.vyi = 0
        self. floorValidPosition = 0

        self.barrelTimer = 0
        self.lifes = 3

        self.marioInitialPos = None
        self.posNotInitialized = True
        self.hammer = False

        self.input = {
        "left":False,
        "right":False,
        "space":False,
        "up":False
        }
    def loadScenery(self):
        self.scene = self.loader.loadModel("models/DKSet1") # only for non animated objects
        self.scene.reparentTo(self.render)

    def setup(self,task):
        lens = OrthographicLens()
        lens.setFilmSize(25, 20)  # Or whatever is appropriate for your scene
        base.camNode.setLens(lens)

        node = self.scene.find("root/camera1")
        node.removeNode()
        self.camera.setPos( 0,30,0 )
        self.camera.lookAt(self.scene)

        self.mario =  self.scene.find("root/mario")
        self.mario.reparentTo(self.scene)

        self.scene.find("root/bottomstair").reparentTo(self.scene)
        self.scene.find("root/floor0").reparentTo(self.scene)
        self.scene.find("root/floor1").reparentTo(self.scene)


        self.scene.find("root/middlestair").reparentTo(self.scene)
        self.scene.find("root/topstair").reparentTo(self.scene)

        self.scene.find("root/floor2").reparentTo(self.scene)
        self.scene.find("root/pCube4").reparentTo(self.scene)
        self.scene.find("root/floors").reparentTo(self.scene)
        self.scene.find("root/barrel").reparentTo(self.scene)

        self.scene.find("root/walls").reparentTo(self.scene)
        self.scene.find("root/rightWall").reparentTo(self.scene)

        self.scene.find("root/MainGroup").reparentTo(self.scene)

        self.barrel = self.scene.find("barrel")
        self.barrel.setPos(self.scene, 0,0,0)


        self.setupCollision()

        base.enableParticles()
        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-9.81) #gravity acceleration
        gravityFN.addForce(gravityForce)
        base.physicsMgr.addLinearForce(gravityForce)

        return Task.done

    def createBarrel(self):

        barrelNode = NodePath("PhysicalBarrel")
        barrelNode.reparentTo(self.scene)

        physicsBarrel = ActorNode("physics_barrel")
        physicsBarrel.getPhysicsObject().setMass(0.01) #in what units? (69 kindda 3 lbs)
        barrel = barrelNode.attachNewNode(physicsBarrel)
        base.physicsMgr.attachPhysicalNode(physicsBarrel)

        barrel.setPos(0,0,2)

        visual_barrel = self.scene.attachNewNode("BarrelCopy")
        originalBarrel = self.scene.find("barrel")
        originalBarrel.instanceTo(visual_barrel)
        visual_barrel.reparentTo(barrel)

        sphere =  CollisionSphere(6.6,0,4.78, 0.5)
        cnodePath = visual_barrel.attachNewNode(CollisionNode('barrelCollider'))
        cnodePath.node().addSolid(sphere)
        cnodePath.node().setFromCollideMask(0xD) # crash with default and mario body and walls
        cnodePath.node().setIntoCollideMask(0xD) # crash with default and mario body and walls
        cnodePath.show()
        self.physicsCollisionPusher.addCollider(cnodePath,barrel)
        base.cTrav.addCollider(cnodePath, self.physicsCollisionPusher)

        barrelForceNode = ForceNode('barrelForce')
        barrel.attachNewNode(barrelForceNode)
        barrelForce = LinearVectorForce(-7,0,0, 1, False)
        # barrelForce.setMassDependent(0)
        barrelForceNode.addForce(barrelForce)
        physicsBarrel.getPhysical(0).addLinearForce(barrelForce)



    def setupBoxCollider(self , node, px, py, pz, w,d,h, nm, colliderEventHandler , fromCollisionMask=0, intoCollisionMask=0  ):

        hitBox = CollisionBox(  Point3(px,py,pz) , w,d,h)
        cnodePath = node.attachNewNode( CollisionNode(nm) )
        cnodePath.node().addSolid(hitBox)
        cnodePath.node().setIntoCollideMask(intoCollisionMask)
        cnodePath.node().setFromCollideMask(fromCollisionMask)
        cnodePath.show()
        base.cTrav.addCollider(cnodePath, colliderEventHandler)


    def setupCollision(self):
        base.cTrav = CollisionTraverser()
        self.collisionHandlerEvent = CollisionHandlerEvent()
        self.physicsCollisionPusher = PhysicsCollisionHandler()

        self.collisionHandlerEvent.addInPattern('into-%in')
        self.collisionHandlerEvent.addOutPattern('outof-%in')

        # create masks
        defaultCollisionMask =      BitMask32(0b0001) #0x1
        segmentCollisionMask =      BitMask32(0b1000) #0x8
        stairsCollisionMask =       BitMask32(0b0010) #0x2
        marioBodyCollisionMask =    BitMask32(0b0011) #0x3
        collisionWallsForBarrels =  BitMask32(0b0100) #0x4


        # mario segment collider
        ray =  CollisionSegment(7,0,-4.5, 7,0,-5.1)
        cnodePath = self.mario.attachNewNode(CollisionNode('marioRay'))
        cnodePath.node().addSolid(ray)
        cnodePath.node().setFromCollideMask(segmentCollisionMask)
        cnodePath.node().setIntoCollideMask(0)
        cnodePath.show()
        base.cTrav.addCollider(cnodePath, self.collisionHandlerEvent)

        self.setupBoxCollider(self.mario, 7,0,-4.5, 0.5,5,0.5, 'marioHitBox', self.collisionHandlerEvent, marioBodyCollisionMask,marioBodyCollisionMask )

        stairs1 =  self.scene.find("bottomstair")
        self.setupBoxCollider(stairs1, -6.8,0,-3.0, 0.5,5,2.5, 'stairs1HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask )

        stairs2 =  self.scene.find("middlestair")
        self.setupBoxCollider(stairs2, -0.86,0, .1, 0.5,5,2.1, 'stairs2HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        stairs3 =  self.scene.find("topstair")
        self.setupBoxCollider(stairs3, -6.8,0, 3.1, 0.5,5,2.2, 'stairs3HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        hammer =  self.scene.find("MainGroup")
        self.setupBoxCollider(hammer, 5.5,0, -1.5, 0.5,5,0.5, 'hammer1HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        floor0 =  self.scene.find("floor0")
        self.setupBoxCollider(floor0, -2.5,0,-5.5, 10,5,0.5, 'floor0HitBox', self.collisionHandlerEvent , intoCollisionMask=segmentCollisionMask )

        floor1 =  self.scene.find("floor1")
        self.setupBoxCollider(floor1, 2,0, -2.5, 8.4,5,0.5, 'floor1HitBox', self.collisionHandlerEvent , intoCollisionMask=segmentCollisionMask )
        floor2_1 =  self.scene.find("floor2")
        self.setupBoxCollider(floor2_1, 3.6,0, 0.5, 3.8,5,0.5, 'floor21HitBox', self.collisionHandlerEvent, intoCollisionMask=segmentCollisionMask )
        floor2_2 =  self.scene.find("pCube4")
        self.setupBoxCollider(floor2_2, -6.3,0, 0.5, 5.0 ,5,0.5, 'floor22HitBox', self.collisionHandlerEvent, intoCollisionMask=segmentCollisionMask )
        floor3 =  self.scene.find("floors")
        self.setupBoxCollider(floor3, 1.8,0, 3.5, 8,5,0.5, 'floor3HitBox',  self.collisionHandlerEvent , intoCollisionMask=segmentCollisionMask )

        rightWall = self.scene.find("rightWall")
        self.setupBoxCollider(rightWall, -12,0, 0, 1,5,10, 'rightWallHitBox',  self.collisionHandlerEvent , fromCollisionMask=collisionWallsForBarrels, intoCollisionMask=collisionWallsForBarrels )

        leftWall = self.scene.find("walls")
        self.setupBoxCollider(leftWall, 11.5,0, 0, 1,5,10, 'leftWallHitBox',  self.collisionHandlerEvent , fromCollisionMask=collisionWallsForBarrels, intoCollisionMask=collisionWallsForBarrels )


        barrelFixer = self.scene.attachNewNode("barrelFixer")
        self.setupBoxCollider(barrelFixer, -3,0, 0.505, 10,5,0.5, 'barrelFixerHitBox',  self.collisionHandlerEvent , fromCollisionMask=collisionWallsForBarrels, intoCollisionMask=collisionWallsForBarrels )

        barrelDestroyer = self.scene.attachNewNode("barrelDestroyer")
        self.setupBoxCollider(barrelDestroyer, 0,0, -8, 15,5,0.5, 'barrelDestroyerHitBox',  self.collisionHandlerEvent , fromCollisionMask=collisionWallsForBarrels, intoCollisionMask=collisionWallsForBarrels )


        self.accept('into-stairs1HitBox', self.enableStair)
        self.accept('outof-stairs1HitBox', self.disableStair)
        self.accept('into-stairs2HitBox', self.enableStair)
        self.accept('outof-stairs2HitBox', self.disableStair)
        self.accept('into-stairs3HitBox', self.enableStair)
        self.accept('outof-stairs3HitBox', self.disableStair)
        self.accept('into-hammer1HitBox', self.enableHammer)

        self.accept('into-floor0HitBox', self.enableJump)
        self.accept('outof-floor0HitBox', self.disableJump)
        self.accept('into-floor1HitBox', self.enableJump)
        self.accept('outof-floor1HitBox', self.disableJump)
        self.accept('into-floor21HitBox', self.enableJump)
        self.accept('outof-floor21HitBox', self.disableJump)
        self.accept('into-floor22HitBox', self.enableJump)
        self.accept('outof-floor22HitBox', self.disableJump)
        self.accept('into-floor3HitBox', self.enableJump)
        self.accept('outof-floor3HitBox', self.disableJump)

        self.accept("into-barrelCollider", self.barrelCrash)

        base.cTrav.showCollisions(self.render)

    def enableHammer(self, evt):
        print(f"{evt.getIntoNodePath()}{evt.getFromNodePath()}")
        self.scene.node().removeChild(evt.getIntoNodePath().node().getParent(0))
        self.hammer = True

    def changeBarrelDirection(self, evt):
        print(f"Changing barrel direction {evt}")

    def barrelCrash(self,evt):
        barrel = evt.getIntoNodePath().node().getParent(0).getParent(0)
        other = evt.getFromNodePath().node().getParent(0)

        parents = barrel.parents
        print(f"{other}")

        if other.name=="barrelDestroyer":
            p = parents[0]
            self.scene.node().removeChild(p)
            return

        if not (other==self.mario.node() or other.name=="barrelFixer" ) :
            forceNode = barrel.getChildren()[1]
            actualForce = forceNode.getForce(0)
            actualForce.setVector( actualForce.getLocalVector().x*-1, 0 , 0 )
            forceNode.clear()
            forceNode.addForce(actualForce)


        if( other == self.mario.node() ):
            if not self.hammer:
                self.lifes = self.lifes - 1
                self.floorValidPosition = 0
                self.mario.setPos(self.scene, self.marioInitialPos)

            p = parents[0]
            self.scene.node().removeChild(p)

            if(  self.lifes < 0):
                print("game over dude!!")


    def enableStair(self, evt):
        print("crashed mario and stair");
        self.canClimb = True

    def disableStair(self, evt):
        print("exit mario and stair");
        self.canClimb = False

    def enableJump(self, evt):
        self.isGrounded = True
        print("enable jump")
        # fromCollider =  evt.getFrom().getCenter().z - evt.getFrom().getDimensions().z/2
        self.floorValidPosition = evt.getInto().getCenter().z + 5.5
        #print(f"{ evt.getInto().getCenter().z } {self.floorValidPosition} ")

    def disableJump(self, evt):
        print("disable jump")
        self.isGrounded = False

    def pressUp(self):
        print("up enabled")
        self.input["up"] = True;

    def stopUp(self):
        print("up disabled")
        self.input["up"] = False;

    def pressRight(self):
        self.input["right"] = True;

    def stopRight(self):
        self.input["right"] = False;

    def pressLeft(self):
        self.input["left"] = True;

    def stopLeft(self):
        self.input["left"] = False;

    def pressSpace(self):
        self.input["space"] = True;
        self.camera.setPos( 0,30,0 )
        self.camera.lookAt(self.scene)

    def stopSpace(self):
        self.input["space"] = False;

    def getAdvance(self):
        if self.input["left"] and self.input["right"]:
            return 0
        if self.input["left"]:
            return -1
        if self.input["right"]:
            return 1
        return 0

    def applyJump(self):
        jz = 0  # jump Y/Z
        vi = 4 # initial velocity
        g = -6 # gravity

        if(self.isGrounded):
            if(self.canJump):
                if(self.input["space"]):
                    self.jumpTime = 0.1
                    self.canJump = False
                    self.vyi = vi
                    jz = self.vyi*self.jumpTime  + 0.5*g*self.jumpTime*self.jumpTime
                    vz = self.vyi + g*self.jumpTime
                else:
                    return 0
            else:
                self.jumpTime = self.jumpTime + globalClock.getDt()
                jz = self.vyi*self.jumpTime  + 0.5*g*self.jumpTime*self.jumpTime
                vz = self.vyi + g*self.jumpTime
                if vz < 0: #finished
                    self.jumpTime = 0
                    self.canJump = True
                    self.vyi = 0
                    jz = 0
        else:
            if(not self.isClimbing):
                self.canJump = False
                self.jumpTime = self.jumpTime + globalClock.getDt()
                jz = self.vyi*self.jumpTime  + 0.5*g*self.jumpTime*self.jumpTime
                vz = self.vyi + g*self.jumpTime

        return jz
    def applyStairs(self, pz):
        if( self.canClimb):
            if(self.input["up"]):
                self.isClimbing = True

        if( self.isClimbing ):
            if( self.input["up"]):
                return pz + 0.1
        if( not self.canClimb):
            self.isClimbing = False

        return pz
    def update(self,task):
        self.camera.setPos( 0,30,0 )
        self.camera.lookAt(self.scene)
        pz = self.applyJump()

        if( self.posNotInitialized):
            self.marioInitialPos = self.mario.getPos()
            self.posNotInitialized = False

        self.barrelTimer = self.barrelTimer + globalClock.getDt()
        if self.barrelTimer > (3 + random()*2):
            self.createBarrel()
            self.barrelTimer = 0

        # self.mario.getPos(self.render).z
        advZ = self.applyStairs(self.floorValidPosition )
        self.floorValidPosition = advZ
        #print(f' {self.mario.getPos(self.render).z} {self.floorValidPosition}  ')
        self.mario.setPos(self.render, self.mario.getPos().x + -self.getAdvance()*.1 , 0 ,advZ+pz)
        return Task.cont

app = DKGame()
app.run()
