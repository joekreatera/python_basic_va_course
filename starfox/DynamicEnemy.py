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
    def __init__(self, pos, world, pandaObject, player, type=ENEMY_TYPE.DEFAULT, shoot=ENEMY_SHOOTER.SHOOTER):
        self.gameObject = pandaObject.copyTo(world)
        self.gameObject.setPos(pos)
        self.player= player
        self.type = type
        self.world = world
        self.shoot = shoot
        self.state = ENEMY_STATE.IDLE
        self.gameObject.setName("dynamicEnemy")

    def update(self, dt):
        print("enemy")
        return 0

    def crash(evt):
        return 0
