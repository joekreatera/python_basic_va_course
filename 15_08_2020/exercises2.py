"""

Estas haciendo un PONG y la mecanica dice:

1- Si la pelota esta por detras del enemigo y la cantidad de puntos es 5 o han habido
3 puntos sin respuesta, el juego tendra como ganador al Usuario
2. El caso inverso es igual, solo que no toma en cuenta la condicion de 3 puntos sin respuesta
3. Si ambos están en 4 puntos , el maximo de puntos debe subir a 6 y por ende el ccaso
(1) y (2) se deberan actualizar.


    |               |
    |               |
    |  1    o    E  |
    |  1         E  |
    |               |
    |               |

"""

px = 3 # player X
ex = 9 # enemy X
bx = 1 # ball X
pp = 2 # player points
ep = 4 # enemy points
w = 2 # 1=player, 2 =CPU
ws = 5
if bx > ex and (pp >= ws or w == 1):
    print("Jugador humano ha ganado")

if bx < px and (ep >= ws or w == 2):
    print("CPU ha ganado")

if (bx > ex or bx < px) and pp == 4 and ep == 4:
    ws = 6
    if( bx > ex):
        pp = pp+1
    else:
        ep = ep+1
    print("Score para ganar es 6")




def testCase(playerX, enemyX, ballX, playerPoints,enemyPoints, wave , winScore):

    if (ballX > enemyX or ballX < playerX) and playerPoints == 4 and ep == 4:
        winScore = winScore + 1
        print("Score para ganar es 6")

    if ballX > enemyX and (playerPoints >= winScore or wave == 1):
        print("Jugador humano ha ganado")

    if ballX < playerX and (enemyPoints >= winScore or wave == 2):
        print("CPU ha ganado")

    if ballX > enemyX:
        playerPoints = playerPoints+1
    if ballX < playerX:
        enemyPoints = enemyPoints+1

    return playerPoints, enemyPoints, winScore

print("Set pp ep ws")
pp,ep,ws = testCase(3,9,1,0,0,0,5)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,10,pp,ep,0,ws)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,10,pp,ep,0,ws)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,1,pp,ep,0,ws)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,1,pp,ep,0,ws)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,10,pp,ep,0,ws)
print(f'Set {pp},{ep},{ws}')
pp,ep,ws = testCase(3,9,10,pp,ep,0,ws)
