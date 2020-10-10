from enum import Enum

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

    def setTargetPos(self, pos):
        self.targetPos = pos

    def update(self, dt):
        posE = self.gameObject.getPos(self.world)
        posP = self.player.getPos(self.world)

        vec = posP - posE
        if( vec.length() < self.distance):
            self.dir = (self.targetPos-posE).normalize()
            self.state = ENEMY_STATE.CHASE

        if( self.type == ENEMY_TYPE.DEFAULT):
            self.updateABEnemy(dt)


    def updateABEnemy(self, dt):
        if( self.state == ENEMY_STATE.CHASE):
            print(self.dir)
            self.gameObject.setPos(self.world , self.gameObject.getPos(self.world) + self.dir*self.vel*dt )

    def crash(evt):
        return 0
