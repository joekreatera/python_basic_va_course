from panda3d.core import LVector3

class Bullet:
    def __init__(self, world, pos , copyFrom , cTrav, collisionHandler):
        self.gameObject = copyFrom.copyTo(world)
        self.gameObject.setPos(world , pos)
        cTrav.addCollider( self.gameObject.find("**collision*"), collisionHandler )
        self.vel = LVector3(0,0,0)

    def crash(evt):
        print("crash bullet")
