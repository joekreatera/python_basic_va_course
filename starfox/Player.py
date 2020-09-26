from InputManager import InputManager
from random import random
class Player:
    def __init__(self, pandaNode):
        self.gameObject = pandaNode

    def update(self, worldRoot , dt):
        #print(f"updating {InputManager.arrowUp}")
        i = 0
        up = InputManager.isInputDown(InputManager.arrowUp)
        down =  InputManager.isInputDown(InputManager.arrowDown)

        right =  InputManager.isInputDown(InputManager.arrowRight)
        left =  InputManager.isInputDown(InputManager.arrowLeft)

        if( up ):
            self.gameObject.setZ(worldRoot,  self.gameObject.getZ() + 0.1 )
        if( down ):
            self.gameObject.setZ(worldRoot,  self.gameObject.getZ() - 0.1 )
        if( right ):
            self.gameObject.setX(worldRoot,  self.gameObject.getX() + 0.1 )
        if( left ):
            self.gameObject.setX(worldRoot,  self.gameObject.getX() - 0.1 )

    def collisionEnter(self,evt):
        self.gameObject.setColor(random(), random(), random() , 1)
