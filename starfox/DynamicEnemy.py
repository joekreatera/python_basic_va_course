class DynamicEnemy:
    def __init__(self, pos, world, pandaObject, type):
        self.gameObject = pandaObject.copyTo(world)
        self.gameObject.setPos(pos)
        self.type = type

    def update(self, dt):
        return 0

    def crash(evt):
        return 0
