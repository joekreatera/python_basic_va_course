from InputManager import InputManager
from random import random
from math import copysign
class Player:
    def __init__(self, pandaNode):
        self.gameObject = pandaNode
        self.px = 0
        self.pz = 0

    def update(self, worldRoot , dt):
        #print(f"updating {InputManager.arrowUp}")
        i = 0
        up = InputManager.isInputDown(InputManager.arrowUp)
        down =  InputManager.isInputDown(InputManager.arrowDown)

        right =  InputManager.isInputDown(InputManager.arrowRight)
        left =  InputManager.isInputDown(InputManager.arrowLeft)

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

    def collisionEnter(self,evt):
        self.gameObject.setColor(random(), random(), random() , 1)
