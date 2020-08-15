from random import random

def getXTree(a):
    return random()*a

def getYTree(a):
    return random()*a


def setTree(w,l):
    x =  getXTree(w)
    y = getYTree(l)
    print(f'My tree is on x: {x} y:{y}')
# --------------------------------------+

w = int(input("Largo del terreno"))
l = int(input("Ancho del terreno"))

setTree(w,l)
setTree(w,l)
setTree(w,l)
setTree(w,l)
setTree(w,l)
setTree(w,l)


def getFoo():
    return 3

x = getFoo()
