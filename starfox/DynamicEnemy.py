from enum import Enum
from panda3d.core import Vec3

class ENEMY_TYPE(Enum):
    CHASER = 1
    DEFAULT = 0


class ENEMY_STATE(Enum):
    IDLE=1
    CHASE=2
    DEAD=4

class ENEMY_SHOOTER(Enum):
    NO_SHOOT=1
    SHOOTER=2



class DynamicEnemy:
    def __init__(self, pos, world, pandaObject, player, cTrav, colHandler,
                            type=ENEMY_TYPE.DEFAULT, shoot=ENEMY_SHOOTER.SHOOTER, vel=0, distanceToAttack=100):
        self.gameObject = pandaObject.copyTo(world)
        self.gameObject.setPos(pos)
        self.player= player
        self.type = type
        self.world = world
        self.shoot = shoot
        self.state = ENEMY_STATE.IDLE
        self.gameObject.setName("dynamicEnemy")
        self.gameObject.setPythonTag("ObjectController",self)
        cTrav.addCollider( self.gameObject.find("**collision*"), colHandler)
        self.gameObject.find("**collision*").node().setIntoCollideMask(0x2)
        self.gameObject.find("**collision*").node().setFromCollideMask(0x2)
        self.targetPos = None
        self.vel = vel
        self.dir = None
        self.distance = distanceToAttack
        self.shootTimer = 3
        self.shootTime  = 3
        self.updatePositionTimer = 0.5
        self.updatePositionTime = 0.5


    def setTargetPos(self, pos):
        self.targetPos = pos

    def update(self, dt, playerParent):
        self.gameObject.lookAt(self.player)
        posE = self.gameObject.getPos(self.world)
        posP = self.player.getPos(self.world)

        vec = posP - posE
        if(self.state == ENEMY_STATE.IDLE and vec.length() < self.distance):
            if( self.type == ENEMY_TYPE.CHASER):
                self.targetPos = posP
            self.dir = (self.targetPos-posE)
            self.dir.normalize()
            self.state = ENEMY_STATE.CHASE

        if( self.type == ENEMY_TYPE.DEFAULT):
            self.updateABEnemy(dt)

        if( self.type == ENEMY_TYPE.CHASER):
            self.updateChaserEnemy(dt , playerParent)

        if(self.state == ENEMY_STATE.CHASE and self.shoot == ENEMY_SHOOTER.SHOOTER):
            self.shootTimer = self.shootTimer - dt
            if( self.shootTimer <= 0):
                self.shootTimer = self.shootTime
                return True
            return False
        return False

    def updateChaserEnemy(self, dt , playerParent):
        if( self.state == ENEMY_STATE.CHASE):
            self.updatePositionTimer = self.updatePositionTimer - dt
            if(self.updatePositionTimer <= 0):
                v = self.world.getRelativeVector(self.player,Vec3(0,1,0))
                targetPos = self.player.getPos(self.world) + v*60

                self.dir = (targetPos-self.gameObject.getPos(self.world))
                self.dir.normalize()
                self.updatePositionTimer = self.updatePositionTime

            self.gameObject.setPos(self.world,
                                self.gameObject.getPos(self.world) + self.dir*self.vel*dt )



    def updateABEnemy(self, dt):
        if( self.state == ENEMY_STATE.CHASE):
            self.gameObject.setPos(self.world , self.gameObject.getPos(
                                    self.world) + self.dir*self.vel*dt )

    def crash(evt):
        return 0
