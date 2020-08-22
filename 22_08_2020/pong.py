# pong exercise


class Ball:
    def __init__(self,w , h):
        self.px = w/2
        self.py = h/2
        self.vx = 1
        self.vy = 1
        self.ww = w
        self.wh = h

    def updatePos(self , left_pad1, right_pad2):
        tx = self.px + self.vx
        ty = self.py + self.vy

        if( ty > self.wh or ty < 0):
            self.vy = self.vy * -1

        if( tx > self.ww or tx < 0 or tx < left_pad1.px or tx > right_pad2.px ):
            self.vx = self.vx * -1

        self.px = self.px + self.vx
        self.py = self.py + self.vy

    def __str__(self):
        return f'Ball is x:{self.px} y:{self.py}'

class Pad:
    def __init__(self,x,y,h):
        self.px = x
        self.py = y
        self.ph = h
    def updatePos(self , ball):
        self.py = ball.py
    def __str__(self):
        return  f'Pad x:{self.px} y:{self.py} '
class World:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.ball = Ball(w,h)
        self.player_pad = Pad(2,w/2, 3)
        self.enemy_pad = Pad(18, w/2, 3)
    def update(self):
        self.ball.updatePos(self.player_pad, self.enemy_pad)
        self.player_pad.updatePos(self.ball)
        self.enemy_pad.updatePos(self.ball)


    def __str__(self):
        return f'---------\nWorld ({self.width}{self.height}):\n{self.ball}\nplayer_pad{self.player_pad} \nenemy_pad:{self.enemy_pad}'
world = World(20,10)

f= open("data.csv","w")
for i in range(0,140):
    print(world)
    world.update()
    f.write(f'{world.ball.px},{world.ball.py}\n')
f.close()
