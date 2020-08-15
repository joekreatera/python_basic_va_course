# funciones y coondicionales!


"""

En un videojuego, el resultado de una batalla entre dos jugadores
se determina por el residuo de la suma entre dos dados (de 6) y 10.

Es necesario generar un programa que pregunte los datos de los datos de ambos
jugadores y determine quien ganó.


"""
def userInput(userNumber):
    e = int(input(f'Usuario {userNumber}. Dato dado1:')) + int(input(f'Usuario {userNumber}. Dato dado2:'))
    return e%10

d1 = userInput(1)
d2 = userInput(2)

if d1 > d2:
    print(f'Usuario 1 ganó {d1} a {d2}')
else:
    if( d1 == d2):
        print("Nadie gano.... ")
    else:
        print(f'Usuario 2 ganó {d2} a {d1} ')

"""
----------------------------------------------------------
"""
