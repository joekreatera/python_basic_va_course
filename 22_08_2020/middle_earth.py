from random import random
from math import sqrt

class Creature:
    def __init__(self, l = 100, m = 0 , f = 0):
        self.__life = l
        self.__magic = m
        self.__force = f
        self.__magic_m = 0
        self.__force_m = 0
    def getStrength(self):
        return self.__magic/20*(1+self.__magic_m) + self.__force/20*(1+self.__force_m) + random()*10
    def get_life(self):
        return self.__life
    def receive_hit(self, h):
        if( self.__life > 0):
            self.__life = self.__life - h
    def get_magic(self):
        return self.__magic
    def get_force(self):
        return self.__force
    def add_magic_mult(self, extra_m):
        self.__magic =  self.__magic  + extra_m
    def add_force_mult(self, extra_m):
        self.__force =  self.__force  + extra_m
    def __str__(self):
        return f'{self.__life},{self.__magic},{self.__force},{self.__magic_m},{self.__force_m}'

class Elf(Creature):
    def __init__(self):
        super().__init__(l=100,m=10+random()*10, f=5+random()*8)

class Orc(Creature):
    def __init__(self):
        super().__init__(l=100,m=5+random()*5, f=12+random()*5)

class Horde:
    def __init__(self, creature ,w, h,sx,sy):
        self.__px = random()*w
        self.__py = random()*h
        self.__vx = (-1+2*random())*sx
        self.__vy = (-1+2*random())*sy
        self.__creatures = []
        self.__creatures.append(creature)
        self.opponent = None
        self.isBattling = False
        self.finished = False

    def getX(self):
        return self.__px

    def getY(self):
        return self.__py

    def updatePos(self, w, h):

        if self.isBattling :
            return

        tx = self.__px + self.__vx
        ty = self.__py + self.__vy

        if( tx > w or tx < 0 ):
            self.__vx = self.__vx * -1
        if( ty > h or ty < 0 ):
            self.__vy = self.__vy * -1

        self.__px = self.__px + self.__vx
        self.__py = self.__py + self.__vy

    def totalForce(self):
        force = 0
        for i in range(0,  len(self.__creatures) ):
            force = force + self.__creatures[i].get_force()
        return force

    def setHit(self, h):
        to_erase = []
        for i in range(0,  len(self.__creatures) ):
            self.__creatures[i].receive_hit(h)

            if (self.__creatures[i].get_life() <= 0):
                to_erase.append(self.__creatures[i])

        for i in range(0,  len(to_erase) ):
            self.__creatures.remove(to_erase[i])

    def getCreaturesSize(self):
        return len(self.__creatures)

    def doBattle(self):
        myHit = self.totalForce()
        otherHit = self.opponent.totalForce()
        self.opponent.setHit(myHit / self.opponent.getCreaturesSize() )
        self.setHit(otherHit / self.getCreaturesSize() )

        if len(self.__creatures) == 0:
            self.finished =True

        if self.opponent.getCreaturesSize()  == 0:
            self.opponent.finished =True

        if self.finished or self.opponent.finished:
            self.isBattling = False
            self.opponent.isBattling = False
            self.opponent.opponent = None
            self.opponent = None

        if( self.opponent == None):
            print(f'battling wth {self} {self.opponent} {self.finished} ')

    def __str__(self):
        cts = ' & '.join(map(str,self.__creatures))
        cts = '{' + cts  + '}'
        return f'x:{self.__px} y:{self.__py} vx:{self.__vx} vy:{self.__vy} c:{cts}'
class Middle_Earth:
    def __init__(self, w, h):
        self.__width = w
        self.__height = h
        self.elves_hordes = []
        self.orcs_hordes = []
        self.DISTANCE = 7
        self.elves_hordes.append( Horde(Elf(), self.__width, self.__height, 5,5 )  )
        self.elves_hordes.append( Horde(Elf(), self.__width, self.__height, 5,5 )  )
        self.elves_hordes.append( Horde(Elf(), self.__width, self.__height, 5,5 )  )
        self.elves_hordes.append( Horde(Elf(), self.__width, self.__height, 5,5 )  )
        self.elves_hordes.append( Horde(Elf(), self.__width, self.__height, 5,5 )  )

        self.orcs_hordes.append( Horde(Orc(), self.__width, self.__height, 3,3 )  )
        self.orcs_hordes.append( Horde(Orc(), self.__width, self.__height, 3,3 )  )
        self.orcs_hordes.append( Horde(Orc(), self.__width, self.__height, 3,3 )  )
        self.orcs_hordes.append( Horde(Orc(), self.__width, self.__height, 3,3 )  )
        self.orcs_hordes.append( Horde(Orc(), self.__width, self.__height, 3,3 )  )

    def distance( self , a , b):
        x1 = a.getX()
        x2 = b.getX()
        y1 = a.getY()
        y2 = b.getY()
        d = (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)
        return sqrt(d)

    def checkBattles(self):
        for i in range(0, len(self.elves_hordes) ):
            if self.elves_hordes[i].isBattling:
                self.elves_hordes[i].doBattle()
            else:
                for j in range(0, len(self.orcs_hordes) ):
                    if self.distance(self.elves_hordes[i] , self.orcs_hordes[j]) < self.DISTANCE :
                        print(f'************* Hay tiro {self.elves_hordes[i]} {self.orcs_hordes[j]}')
                        if not self.elves_hordes[i].isBattling:
                            self.elves_hordes[i].isBattling = True
                            self.orcs_hordes[j].isBattling = True
                            self.elves_hordes[i].opponent = self.orcs_hordes[j]
                            self.orcs_hordes[j].opponent = self.elves_hordes[i]

    def update(self):
        # check possible battles
        self.checkBattles()

        hordes_to_remove = []
        for i in range(0, len(self.elves_hordes) ):
            self.elves_hordes[i].updatePos( self.__width , self.__height)
            if(  self.elves_hordes[i].finished  ):
                hordes_to_remove.append( self.elves_hordes[i] )

        for i in range(0, len( hordes_to_remove ) ):
            self.elves_hordes.remove( hordes_to_remove[i] )

        hordes_to_remove = []
        for i in range(0, len(self.orcs_hordes) ):
            self.orcs_hordes[i].updatePos( self.__width , self.__height)
            if(  self.orcs_hordes[i].finished  ):
                hordes_to_remove.append( self.orcs_hordes[i] )

        for i in range(0, len( hordes_to_remove ) ):
            self.orcs_hordes.remove( hordes_to_remove[i] )

        #move positions of alive hordes

    def battle(hordeA, hordeB):
        a = 0
    def __str__(self):
        orcs = ' '.join(map(str , self.orcs_hordes ))
        elves = ' '.join(map(str , self.elves_hordes ))
        return f'World!\nOrcs Hordes:\n{orcs} \nElves hords:\n{elves} '

world = Middle_Earth(100,100)
print(world)
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
world.update()
