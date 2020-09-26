from math import pi,cos,sin
from random import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor

from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, CardMaker
from panda3d.core import TextureStage
from panda3d.core import OrthographicLens
from panda3d.core import NodePath
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce,PhysicsCollisionHandler
from panda3d.core import AmbientLight
from panda3d.core import Vec4, LVector3
from panda3d.core import CollisionBox, CollisionSphere
from panda3d.core import CollisionRay, CollisionSegment
from panda3d.core import CollisionNode, BitMask32
from panda3d.core import CollisionTraverser
from panda3d.core import DataNode
from panda3d.core import CollisionHandlerEvent
from panda3d.core import DirectionalLight
from panda3d.core import loadPrcFileData
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "textures-auto-power-2 #f")
loadPrcFileData("", "textures-power-2 none")
loadPrcFileData("", "textures-square none")

class AuxData(DataNode):
    def __init__(self, aName, extraData):
        DataNode.__init__(self, aName)
        DataNode.setPythonTag(self, "subclass", self)
        self.sequence = extraData
        self.frame = 0


class DKGame(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.t = 1
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
        self.floorValidPosition = -4.5

        self.barrelTimer = 0
        self.lifes = 3

        self.marioInitialPos = None
        self.posNotInitialized = True
        self.hammer = False
        self.barrels_frames = []
        self.barrels_frames.append(0)
        self.barrels_frames.append( 0.410573 - 0.375774)
        self.barrels_frames.append( 0.444913 - 0.375774)
        self.barrels_frames.append( 0.479941 - 0.375774)

        self.dk_barrel_sequence = self.createDKBarrelSequence()
        self.hammer_sequence = self.createMarioHammerSequence()
        self.input = {
        "left":False,
        "right":False,
        "space":False,
        "up":False
        }


    def showHammerFrame(self, frame):
        if( frame == 1):
            self.marioRealGraphic.find("hammerup").show()
            self.marioRealGraphic.find("hammerdowm").hide()
        if( frame == 2):
            self.marioRealGraphic.find("hammerdowm").show()
            self.marioRealGraphic.find("hammerup").hide()


    def createMarioHammerSequence(self):
        f1 = Func( self.showHammerFrame , 1  )
        f2 = Func( self.showHammerFrame , 2 )
        delay = Wait(0.1)

        mySequence = Sequence(f1, delay,f2, delay)
        return mySequence


    def changeDKFrame(self, frame):
        dk = self.scene.find("hammer1") #remember that the name is wrong here
        if( frame == 1):
            dk.setTexOffset(TextureStage.getDefault() , 0.140867 - 0.0446603 ,0.0 )
        if( frame == 2):
            dk.setTexOffset(TextureStage.getDefault() , 0.0431023 - 0.0446603 ,  0.806672 - 0.703844 )
        if( frame == 3):
            dk.setTexOffset(TextureStage.getDefault() , 0 ,0.0 )

        """
        frames
        2) 0.140867 0.703844

        1) 0.0431023 0.806672 ;

         throw
        0 0.0446603 0.703065
        """

    def createDKBarrelSequence(self):
        func1 = Func(self.changeDKFrame,1)
        func2 = Func(self.changeDKFrame,2)
        func3 = Func(self.changeDKFrame,3)
        func4 = Func(self.createBarrel)
        delay = Wait(0.5)
        mySequence = Sequence(func1, delay,func2, delay, func3, func4, delay, func1)
        mySequence.loop()
        return mySequence

    def loadScenery(self):
        self.scene = self.loader.loadModel("models/DKSetTextured") # only for non animated objects
        myTexture = loader.loadTexture("models/dk-arcade.png")
        self.scene.setTexture(myTexture)
        self.scene.setTransparency(1)
        self.scene.reparentTo(self.render)

    def setup(self,task):
        lens = OrthographicLens()
        lens.setFilmSize(21.8,18)  # Or whatever is appropriate for your scene
        #lens.setFilmSize(142,136)  # Or whatever is appropriate for your scene

        base.camNode.setLens(lens)

        node = self.scene.find("root/camera1")
        node.removeNode()
        self.camera.setPos( 0,30,0 )
        self.camera.lookAt(self.scene)


        self.mario = self.render.attachNewNode("MarioContainer")
        self.mario.setPos(self.scene, 0,0,0)
        self.marioGraphic = self.mario.attachNewNode("MarioGraphic")
        self.marioGraphic.setPos(self.mario, 0,0,0)
        self.scene.find("root/mario").reparentTo(self.marioGraphic)

        myTexture = loader.loadTexture("models/dk-arcade.png")
        self.marioRealGraphic = self.marioGraphic.find("mario")
        self.marioRealGraphic.setPos(self.marioGraphic, -6.7, 1, 4.5 )
        self.marioRealGraphic.setTexture(myTexture)
        self.marioRealGraphic.setTwoSided(True)
        self.marioRealGraphic.setTransparency(1)


        self.scene.find("root/hammerup").reparentTo(self.marioRealGraphic)
        self.scene.find("root/hammerdowm").reparentTo(self.marioRealGraphic)
        self.marioRealGraphic.find("hammerup").hide()
        self.marioRealGraphic.find("hammerdowm").hide()

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
        self.scene.find("root/hammer1").reparentTo(self.scene)

        self.barrel = self.scene.find("barrel")
        self.barrel.setPos(self.scene, 0,0,20)

        myTexture = loader.loadTexture("models/block.png")
        self.scene.find("floor0").setTexture(myTexture)
        self.scene.find("floor1").setTexture(myTexture)
        self.scene.find("floor2").setTexture(myTexture)
        self.scene.find("floors").setTexture(myTexture)
        self.scene.find("pCube4").setTexture(myTexture)

        self.scene.find("floor0").setTransparency(1)
        self.scene.find("floor1").setTransparency(1)
        self.scene.find("floor2").setTransparency(1)
        self.scene.find("floors").setTransparency(1)
        self.scene.find("pCube4").setTransparency(1)

        myTexture = loader.loadTexture("models/stairs.png")
        self.scene.find("bottomstair").setTexture(myTexture)
        self.scene.find("middlestair").setTexture(myTexture)
        self.scene.find("topstair").setTexture(myTexture)

        self.scene.find("bottomstair").setTransparency(1)
        self.scene.find("middlestair").setTransparency(1)
        self.scene.find("topstair").setTransparency(1)

        base.setBackgroundColor(0,0,0)

        self.setupCollision()

        base.enableParticles()
        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-9.81) #gravity acceleration
        gravityFN.addForce(gravityForce)
        base.physicsMgr.addLinearForce(gravityForce)


        # create dk graphic barrel sequence


        return Task.done


    def barrelGraphicUpdate(self, visual, physics, data):
        def update():
            vel = physics.getPhysicsObject().getVelocity()
            prevFrame = data.node().getPythonTag("subclass").frame
            if( vel.x < 0):
                data.node().getPythonTag("subclass").frame = (prevFrame - 1)%4
            else:
                data.node().getPythonTag("subclass").frame =  (prevFrame + 1)%4

            visual.setTexOffset(TextureStage.getDefault() , self.barrels_frames[prevFrame] ,0.0 )

        return update

    def createBarrelGraphicSequence(self, visual, physics, data):

        funcInterval = FunctionInterval(self.barrelGraphicUpdate(visual, physics, data), name = "BarrelGraphicUpdate")
        delay = Wait(0.1)
        mySequence = Sequence(funcInterval, delay)
        mySequence.loop()
        return mySequence

    def createBarrel(self):

        barrelNode = NodePath("PhysicalBarrel")
        barrelNode.reparentTo(self.scene)
        barrelNode.setPos(self.scene, 0,0,0)
        physicsBarrel = ActorNode("physics_barrel")
        physicsBarrel.getPhysicsObject().setMass(0.01) #in what units? (69 kindda 3 lbs)
        barrel = barrelNode.attachNewNode(physicsBarrel)
        base.physicsMgr.attachPhysicalNode(physicsBarrel)

        barrel.setPos(barrelNode, 0,0,0)

        visual_barrel = self.scene.attachNewNode("BarrelCopy")
        originalBarrel = self.scene.find("barrel")
        originalBarrel.instanceTo(visual_barrel)
        visual_barrel.reparentTo(barrel)
        visual_barrel.setPos(self.scene, -6.5,0,-24.5 )

        dataNode = barrelNode.attachNewNode(AuxData("Sequence",None))
        seq = self.createBarrelGraphicSequence(visual_barrel, physicsBarrel, dataNode)
        dataNode.node().getPythonTag("subclass").sequence = seq

        #sphere =  CollisionSphere(6.6,0,4.78, 0.5)
        sphere =  CollisionSphere(6.6,0,24.7, 0.5)
        cnodePath = visual_barrel.attachNewNode(CollisionNode('barrelCollider'))
        cnodePath.node().addSolid(sphere)
        cnodePath.node().setFromCollideMask(0xD) # crash with default and mario body and walls
        cnodePath.node().setIntoCollideMask(0xD) # crash with default and mario body and walls
        self.showCollision(cnodePath)
        #cnodePath.show()
        self.physicsCollisionPusher.addCollider(cnodePath,barrel)
        base.cTrav.addCollider(cnodePath, self.physicsCollisionPusher)

        barrelForceNode = ForceNode('barrelForce')
        barrel.attachNewNode(barrelForceNode)
        barrelForce = LinearVectorForce(-7,0,0, 1, False)
        # barrelForce.setMassDependent(0)
        barrelForceNode.addForce(barrelForce)
        physicsBarrel.getPhysical(0).addLinearForce(barrelForce)
        # starting barrel point :D
        barrelNode.setPos(self.scene,6.5,0,4.5)

    def setupBoxCollider(self , node, px, py, pz, w,d,h, nm, colliderEventHandler , fromCollisionMask=0, intoCollisionMask=0  ):

        hitBox = CollisionBox(  Point3(px,py,pz) , w,d,h)
        cnodePath = node.attachNewNode( CollisionNode(nm) )
        cnodePath.node().addSolid(hitBox)
        cnodePath.node().setIntoCollideMask(intoCollisionMask)
        cnodePath.node().setFromCollideMask(fromCollisionMask)
        # cnodePath.show()
        self.showCollision(cnodePath)

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
        #ray =  CollisionSegment(7,0,-4.5, 7,0,-5.1)
        ray =  CollisionSegment(0,0,0, 0,0,-.51)
        cnodePath = self.mario.attachNewNode(CollisionNode('marioRay'))
        cnodePath.node().addSolid(ray)
        cnodePath.node().setFromCollideMask(segmentCollisionMask)
        cnodePath.node().setIntoCollideMask(0)
        self.showCollision(cnodePath)
        base.cTrav.addCollider(cnodePath, self.collisionHandlerEvent)

        #self.setupBoxCollider(self.mario, 7,0,-4.5, 0.5,5,0.5, 'marioHitBox', self.collisionHandlerEvent, marioBodyCollisionMask,marioBodyCollisionMask )
        self.setupBoxCollider(self.mario, 0,0,0, 0.5,5,0.5, 'marioHitBox', self.collisionHandlerEvent, marioBodyCollisionMask,marioBodyCollisionMask )


        stairs1 =  self.scene.find("bottomstair")
        self.setupBoxCollider(stairs1, -6.8,0,-3.0, 0.5,5,2.5, 'stairs1HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask )

        stairs2 =  self.scene.find("middlestair")
        self.setupBoxCollider(stairs2, -0.86,0, .1, 0.5,5,2.1, 'stairs2HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        stairs3 =  self.scene.find("topstair")
        self.setupBoxCollider(stairs3, -6.8,0, 3.1, 0.5,5,2.2, 'stairs3HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        hammer =  self.scene.find("MainGroup") # hammer
        self.setupBoxCollider(hammer, 5.5,0, -1.5, 0.5,5,0.5, 'hammer1HitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

        dk =  self.scene.find("hammer1")
        self.setupBoxCollider(dk, 8.7,0, 5, 1,5,1, 'dkHitBox', self.collisionHandlerEvent, stairsCollisionMask,stairsCollisionMask  )

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
        self.accept('into-dkHitBox', self.dkArrived)

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

        #base.cTrav.showCollisions(self.render)

    def showCollision(self, col):
        #col.show()
        print("Not showing collider")

    def dkArrived(self,evt):
        if(self.hammer):
            self.scene.node().removeChild(evt.getIntoNodePath().node().getParent(0))
            text = DirectLabel(text="You won", text_scale=(0.5,0.5))
        else:
            self.floorValidPosition = -4.5
            self.mario.setPos(self.scene, self.marioInitialPos)
            text = DirectLabel(text="Game Over", text_scale=(0.5,0.5))


    def enableHammer(self, evt):
        print(f"{evt.getIntoNodePath()}{evt.getFromNodePath()}")
        self.scene.node().removeChild(evt.getIntoNodePath().node().getParent(0))
        self.hammer_sequence.loop()
        self.hammer = True

    def changeBarrelDirection(self, evt):
        print(f"Changing barrel direction {evt}")


    def barrelCrash(self,evt):
        barrel = evt.getIntoNodePath().node().getParent(0).getParent(0)
        other = evt.getFromNodePath().node().getParent(0)

        parents = barrel.parents
        # print(f"{other}")

        if other.name=="barrelDestroyer":
            p = parents[0]
            childrens = barrel.getParent(0).getChildren()
            childrens[1].getPythonTag("subclass").sequence.finish()
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
                self.floorValidPosition = -4.5
                self.mario.setPos(self.scene, self.marioInitialPos)

            p = parents[0]
            childrens = barrel.getParent(0).getChildren()
            childrens[1].getPythonTag("subclass").sequence.finish()
            self.scene.node().removeChild(p)

            if(  self.lifes < 0):
                print("game over dude!!")
                text = DirectLabel(text="Game Over", text_scale=(0.5,0.5))

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

        self.floorValidPosition = evt.getInto().getCenter().z + 1
        print(f"{ evt.getInto().getCenter().z } {self.floorValidPosition} ")

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
        #self.camera.setPos( 0,30,0 )
        #self.camera.lookAt(self.scene)

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
        if self.barrelTimer > (3 + random()*2):  # fix error! when dk has lost! -> exercise :D
            self.dk_barrel_sequence.start()
            self.barrelTimer = 0

        # self.mario.getPos(self.render).z
        advZ = self.applyStairs(self.floorValidPosition )
        self.floorValidPosition = advZ

        if( self.getAdvance() != 0):
            self.marioGraphic.setSx(self.mario, -self.getAdvance())

        self.mario.setPos(self.render, self.mario.getPos().x + -self.getAdvance()*.1 , 0 , advZ+pz ) # advZ+pz

        return Task.cont


app = DKGame()
app.run()
