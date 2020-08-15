# funciones y coondicionales!


"""

En un videojuego, el resultado de una batalla entre dos jugadores
se determina por el residuo de la suma entre dos dados (de 6) y 10.

Es necesario generar un programa que pregunte los datos de los datos de ambos
jugadores y determine quien ganó.


"""

e1 = int(input("Usuario1. Dato dado1:")) + int(input("Usuario1. Dato dado2:"))
e2 = int(input("Usuario2. Dato dado1:")) + int(input("Usuario2. Dato dado2:"))

d1 = e1%10
d2 = e2%10

if d1 > d2:
    print(f'Usuario 1 ganó {d1} a {d2}')
else:
    print(f'Usuario 2 ganó {d2} a {d1} ')

"""
----------------------------------------------------------
"""


d1 = int(input("Player1. Dado 1: "))
d12 = int(input("Player1. Dado 2: "))
d2 = int(input("Player2. Dado 1: "))
d22 = int(input("Player2. Dado 2: "))
r1 = d1 + d12 % 10
r2 = d2 + d22 % 10
if r1 > r2:
    print("Gana el Player 1 ")
else r2 > r1:
    print("Gana Player 2")
