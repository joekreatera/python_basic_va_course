from random import random

def getXTree(a,b):
    return a + random()*(b-a)

def getYTree(a,b):
    return a + random()*(b-a)

def setTree(w,l,min_val, max_val):
    x =  getXTree(w*min_val,w*max_val)
    y = getYTree(l*min_val,l*max_val)
    print(f'My tree is on x: {x} y:{y}')

w = int(input("Largo del terreno"))
l = int(input("Ancho del terreno"))

pct = 1/6
setTree(w,l,pct*1,pct*2)
setTree(w,l,pct*2,pct*3)
setTree(w,l,pct*3,pct*4)
setTree(w,l,pct*4,pct*5)
setTree(w,l,pct*5,pct*6)
setTree(w,l,pct*0,pct*1)
