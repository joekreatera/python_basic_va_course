force = 0
cost = 0
force = int(input('Fuerza base:'))
cost = int(input('Costo base:'))

fire_armor = int(input('Armadura de fuego? (1)Si (0)No'))
force = force - fire_armor*10
cost = cost + fire_armor*5

enforced_armor = int(input('armadura reforzada? (1)Si (0)No'))
force = force - enforced_armor*5
cost = cost + enforced_armor*10

sword = int(input('Espada de singularidad? (1)Si (0)No'))
force = force + sword*7
cost = cost + sword*10

shield = int(input('Escudo nova? (1)Si (0)No'))
cost = cost + 10

juice =  int(input('Jugo aceitoso? (1)Si (0)No'))
force = force + juice*10
cost = cost + 8


print('Fuerza ' + str(force) )
print('Costo ' + str(cost) )
