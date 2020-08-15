from math import sqrt

print('Collision test')


x1 = int(input('X1:'))
y1 = int(input('Y1:'))
r1 = int(input('R1:'))


x2 = int(input('X2:'))
y2 = int(input('Y2:'))
r2 = int(input('R2:'))

dfx = x1 - x2
dfx = dfx * dfx

dfy = y1 - y2
dfy = dfy * dfy

df = dfx + dfy

r = sqrt(df)
sr= r1+r2
if r < sr:
    print("Chocaron")
else:
    print("Todo bien")
