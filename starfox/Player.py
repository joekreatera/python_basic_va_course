from InputManager import InputManager
from random import random
from math import copysign
class Player:
    def __init__(self, pandaNode , collisionMask = 0x01):
        self.gameObject = pandaNode
        self.px = 0
        self.pz = 0
        self.prepareShoot = False
        self.shoot  = False

    def getShoot(self):
        if( self.shoot):
            self.shoot = False
            return True
        return False

    def update(self, worldRoot , dt):
        #print(f"updating {InputManager.arrowUp}")


        i = 0
        up = InputManager.isInputDown(InputManager.arrowUp)
        down =  InputManager.isInputDown(InputManager.arrowDown)

        right =  InputManager.isInputDown(InputManager.arrowRight)
        left =  InputManager.isInputDown(InputManager.arrowLeft)

        space = InputManager.isInputDown(InputManager.space)
        if( self.prepareShoot == True and space == False):
            self.shoot = True
            self.prepareShoot = False
        if( self.prepareShoot == False and space == True):
            self.shoot = False
            self.prepareShoot = True


        vel = 20
        maxXPos = 24
        maxZPos = 12

        if( up ):
            self.pz = self.pz + vel*dt
        if( down ):
            self.pz = self.pz - vel*dt
        if( right ):
            self.px = self.px + vel*dt
        if( left ):
            self.px = self.px - vel*dt


        self.pz = max( -maxZPos , min(maxZPos, self.pz))
        self.px = max( -maxXPos , min(maxXPos, self.px))

        self.gameObject.setZ(worldRoot,  self.pz )
        self.gameObject.setX(worldRoot,  self.px )

        extraX = self.px
        extraZ = self.pz
        thresholdX = 8
        thresholdZ = 5

        if( abs(extraX) > thresholdX):
            extraX = (abs(extraX) - thresholdX)*copysign(1,extraX)
        else:
            extraX = 0
        if( abs(extraZ) > thresholdZ):
            extraZ = (abs(extraZ) - thresholdZ)*copysign(1,extraZ)
        else:
            extraZ = 0

        return extraX, extraZ

    def crash(self,evt):
        self.gameObject.setColor(random(), random(), random() , 1)
