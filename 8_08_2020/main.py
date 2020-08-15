# programa para obtener mi edad en 10 años
"""
Este es un comentario
de varias lineas para poder
demostrar
"""
name = input('Nombre:')
age = input('Edad:')
age10 = int(age)+10
line = 'Hola ' + name + ' en 10 años tendras ' + str(age10)
print( line )

"""
Estas programando un juego de batallas de robots
Tu robot debe ser configurado para calcular su fuerza
y el costo de su armadura
Si el robot quiere armadura de fuego su fuerza decrece en 10
    su costo aumenta en 5
Si el robot quiere armadura reforzada su fuerza decrece en 5
    su costo aument en 10
Si el robot quiere espada de la singularidad fuerza aumenta en 7
    su costo aumenta en 10
Si el robot quiere escudo nova su fuerza no se modifica
    su costo aumenta en 10
Si el robot quiere jugo aceitoso, su fuerza aumenta en 10
    su costo aumenta en 8

El programa debe empezar por fuerza y costo que el usuario
decida e ir preguntando lo necesario
"""
