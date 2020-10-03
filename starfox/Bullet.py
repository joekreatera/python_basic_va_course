from panda3d.core import LVector3

class Bullet:
    def __init__(self, world, pos , copyFrom , cTrav, collisionHandler):
        self.gameObject = copyFrom.copyTo(world)
        self.gameObject.setPos(world , pos)
        cTrav.addCollider( self.gameObject.find("**collision*"), collisionHandler )
        self.vel = LVector3(0,0,0)
        self.gameObject.setPythonTag("ObjectController" , self )
        self.world = world
        self.gameObject.setName("bullet")

    def update(self ,dt ):
        print("update ")
        self.gameObject.setPos(self.world , 0,0,0)

    def crash(self, evt):
        print("crash bullet")
