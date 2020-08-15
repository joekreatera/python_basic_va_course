# distance between points and
from math import *
def distance(xa,ya,xb,yb):
    dx = xa - xb
    dy = ya - yb
    d = sqrt(dx**2 + dy**2)
    return d
x1 = int(input('X1:'))
y1 = int(input('Y1:'))
x2 = int(input('X2:'))
y2 = int(input('Y2:'))
x3 = int(input('X3:'))
y3 = int(input('Y3:'))
d = distance(x1, y1, x2, y2)
print("Distancia 1: " + str(d))
d = distance(x1, y1, x3, y3)
print("Distancia 2: " + str(d))
d = distance(x2, y2, x3, y3)
print("Distancia 3: " + str(d))
