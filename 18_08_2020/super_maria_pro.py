class Game_object:
    def __init__(self,x=0,y=0):
        self.__x = x
        self.__y = y
    def set_x(self,x):
        self.__x = x
    def set_y(self,y):
        self.__y = y
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y
    def __str__(self):
        return f'Lugar: {self.get_x()} y {self.get_y()}'

class Maria(Game_object):
    def __init__(self, x, y):
        super().__init__(x,y)

class Block(Game_object):
    def __init__(self, x, y):
        super().__init__(x,y)

class Enemy(Game_object):
    def __init__(self, x, y, min_limit_x, min_limit_y, max_limit_x, max_limit_y):
        super().__init__(x,y)
        self.__min_limit_x = min_limit_x
        self.__min_limit_y = min_limit_y
        self.__max_limit_x = max_limit_y
        self.__max_limit_y = max_limit_y


class Hortuga(Enemy):
    def __init__(self, x,y,min_block, max_block):
         super().__init__(x,y,min_block.get_x() , min_block.get_y(), max_block.get_x() , max_block.get_y() )

class Pambooza(Enemy):
    def __init__(self, x,y, min_limit_x, min_limit_y, max_limit_x, max_limit_y):
         super().__init__(x,y,min_limit_x, min_limit_y, max_limit_x, max_limit_y )

class World():
    def __init__(self):
        self.maria = Maria(1,1)
        self.block1 = Block(10,1)
        self.block2 = Block(20,1)
        self.hort1 = Hortuga(15,1,self.block1,self.block2)
        self.pamb1 = Pambooza(30,1,21,1,37,1)

    def step(self):
        mx = self.maria.get_x() + 1
        if( mx <= 100 ): # limite del mundo
            self.maria.set_x(mx)

    def __str__(self):
        res = '------------------------\n'
        res = res + (f'Maria: {self.maria} \n')
        res = res + (f'B1_{self.block1} \n')
        res = res + (f'B2:{self.block2} \n')
        res = res + (f'H1:{self.hort1} \n')
        res = res + (f'P1:{self.pamb1} \n')
        return res

world = World()
print(f'{world}')
world.step()
print(f'{world}')
world.step()
print(f'{world}')
world.step()
print(f'{world}')
world.step()
print(f'{world}')
world.step()
print(f'{world}')


my_list = [1,23,4,5,6]
my_list.append(9)
print(my_list)
my_list.pop()
print(my_list)

my_list = [1,23,4,5,6]
for i in range(0,len(my_list) ):
    s = my_list[i]+1
    print(str(s))

print(my_list[1])
