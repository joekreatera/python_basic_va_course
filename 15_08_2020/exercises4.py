#cards!!!

"""


Función de múltiple retorno de valor: genera una función que reciba un
valor (corazones-1, picas-2, tréboles-3, diamantes-4) y entregue tres cartas del
as al rey.


"""
from random import random

def getCards(f):
    a = int(random()*12+1)
    b = int(random()*12+1)
    c = int(random()*12+1)
    return a,b,c

cp = 2
c1,c2,c3 = getCards(cp)

print(f'{c1} {cp}')
print(f'{c2} {cp}')
print(f'{c3} {cp}')
