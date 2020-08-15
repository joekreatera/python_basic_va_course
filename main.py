from random import random

dec = input("Caverna (c) o Bosque (b): ")

if dec == 'c':
    if random() <= 0.20 :
        print("Has muerto por un oso")
    else:
        print("Has vivido para morir otro dia")


if dec == 'b':
    if random() <= 0.40:
        print("Has muerto de frío")
    else:
        print("Has vivido para morir otro dia")


dec = input("Caverna (c) o Bosque (b): ")
cond = dec == 'c'
valor = -23
if (valor):
    print("elegiste caverna")


sw = int(input('Tu personaje tiene espada:0-No 1-Si-'))
sh = int(input('Tu personaje tiene escudo:0-No 1-Si-'))
lf = int(input('Tu personaje tiene vida disponible:0-No 1-Si-'))

if sw==1 and sh==1 and lf==1:
    print('Tienes todo, a luchar!')

if sw==1 or sh==1 or lf==1:
    print('Al menos algo!')


if sw==1 and sh==1 or lf==1:
    print('Cuentas con el equipo pero la vida no vale nada!')

if sw==1 or sh==1 and lf==1:
    print('Traes algo, pero mucha vida y corazonas')

if sw != 0:
    print('Traes espada!!!!')

if not(sw == 1 and sh == 1):
    print('-------------------> No traes ambos!!!')

if sw == 0 and sh == 0:
    print("Vas muy desprotegido")
if sw == 0 and sh == 1:
    print("Suerte atacando jajaj")
if sw == 1 and sh == 0:
    print("Te va a doler pero vas a herir")
if sw == 1 and sh == 1:
    print("Con todo muchacho")

if sw==1 or sh==1:
    print("Al menos no vas en blanco")


if sw == 1 :
    if sh == 0:
        print("solo espada!")
    else:
        print("ambos")



def killEnemy(force, enemy_life, amulet=0, force_kill=False, print_final_life=False):

    if amulet == 0:
        final_life = enemy_life - force
    if amulet == 1:
        final_life = enemy_life - force*1.5

    if print_final_life :
        print("Enemy final life " + str(final_life) )
    if final_life > 0:
        return False
    return True

enemy= 100
myforce = 70
first_enemy = killEnemy(myforce, enemy)
# got amulet
am = 1
second_enemy = killEnemy(myforce, enemy, am)
third_enemy = killEnemy(myforce, enemy, am, print_final_life=True)
print(f'Estado de los enemigos {first_enemy} Y {second_enemy} Y {third_enemy}')
