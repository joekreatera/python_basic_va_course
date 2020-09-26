from InputManager import InputManager
class Player:
    def __init__(self, pandaNode):
        self.gameObject = pandaNode

    def update(self, worldRoot , dt):
        #print(f"updating {InputManager.arrowUp}")
        i = 0
