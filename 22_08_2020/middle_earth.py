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
    def __init__(self, creature):
        self.__px = 0
        self.__py = 0
        self.__vx = 0
        self.__vy = 0
        self.__creatures = []
        self.__creatures.append(creature)

    def __str__(self):
        cts = ' & '.join(map(str,self.__creatures))
        cts = '{' + cts  + '}'
        return f'x:{self.__px} y:{self.__py} vx:{self.__vx} vy:{self.__vy} c:{cts}'
class Middle_Earth:
    def __init__(self):
        self.elves_hordes = []
        self.orcs_hordes = []

        self.elves_hordes.append( Horde(Elf() )  )
        self.orcs_hordes.append( Horde(Orc() ) )
        self.orcs_hordes.append( Horde(Orc() ) )

    def update(self):
        # check possible battles
        a = 0
        #move positions of alive hordes
    def battle(hordeA, hordeB):
        a = 0
    def __str__(self):
        orcs = ' '.join(map(str , self.orcs_hordes ))
        elves = ' '.join(map(str , self.elves_hordes ))
        return f'World!\nOrcs Hordes:\n{orcs} \nElves hords:\n{elves} '
world = Middle_Earth()
print(world)
