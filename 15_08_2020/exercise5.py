class Helado:
    sabor_bola_1 = ""
    px = 0
    py = 0

chokoHelado = Helado()
chokoHelado.sabor_bola_1 = "Chokolate"

zarzaHelado = Helado()
zarzaHelado.sabor_bola_1 = "Zarzamora"

print( chokoHelado.sabor_bola_1)
print( zarzaHelado.sabor_bola_1)


"""
Fuerza = altura ((1,3) /3) *0.6 + escudo(10,22)/22*0.3 + poder_especial(7,9)/9*0.1
"""
from random import random
class Robot:
    def __init__(self, alt=1, esc=10, pes=7):
        self.altura = alt
        self.escudo = esc
        self.poder_especial = pes
    def fuerza(self):
        return self.altura/3*0.6 + self.escudo/22*0.3 + self.poder_especial/9*0.1

def valor(min, max):
    return random()*(max-min)+min

r1 = Robot(valor(1,3),valor(10,22),valor(7,9))
r2 = Robot(valor(1,3),valor(10,22),valor(7,9))
r3 = Robot(esc=15, alt=3)
f1 = r1.fuerza()
f2 = r2.fuerza()
if  f1>f2:
    print(f'Robot 1 con {f1}')
else:
    print(f'Robot 2 con {f2}')
