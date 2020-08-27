from random import random

class Creature:
    def __init__(self, l = 100, m = 0 , f = 0):
        self.__life = l
        self.__magic = m
        self.__force = f
        self.__magic_m = 0
        self.__force_m = 0
    def getStrength(self):
        return self.magic/20*(1+self.magic_m) + self.force/20*(1+self.force_m) + random()*10
    def get_life(self):
        return self.__life
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

    def updatePos(self, w, h):
        tx = self.__px + self.__vx
        ty = self.__py + self.__vy

        if( tx > w or tx < 0 ):
            self.__vx = self.__vx * -1
        if( ty > h or ty < 0 ):
            self.__vy = self.__vy * -1

        self.__px = self.__px + self.__vx
        self.__py = self.__py + self.__vy


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

    def update(self):
        # check possible battles

        for i in range(0, len(self.elves_hordes) ):
            self.elves_hordes[i].updatePos( self.__width , self.__height)

        for i in range(0, len(self.orcs_hordes) ):
            self.orcs_hordes[i].updatePos( self.__width , self.__height)

        #move positions of alive hordes

    def battle(hordeA, hordeB):
        a = 0
    def __str__(self):
        orcs = ' '.join(map(str , self.orcs_hordes ))
        elves = ' '.join(map(str , self.elves_hordes ))
        return f'World!\nOrcs Hordes:\n{orcs} \nElves hords:\n{elves} '

world = Middle_Earth(100,100)
print(world)
