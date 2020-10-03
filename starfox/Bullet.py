from panda3d.core import Vec3

class Bullet:
    def __init__(self, world, pos , copyFrom , cTrav, collisionHandler, fwd):
        self.gameObject = copyFrom.copyTo(world)
        self.gameObject.setPos(world , pos)
        cTrav.addCollider( self.gameObject.find("**collision*"), collisionHandler )
        self.vel = fwd
        self.gameObject.setPythonTag("ObjectController" , self )
        self.world = world
        self.gameObject.setName("bullet")

    def update(self ,dt ):
        print("update ")
        p = self.gameObject.getPos(self.world)
        self.gameObject.setPos(self.world ,
                    p.x+self.vel.x*4 ,
                    p.y+self.vel.y*4 ,
                    p.z+self.vel.z*4 )

    def crash(self, evt):
        print("crash bullet")
