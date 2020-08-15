# funciones

"""
Función de retorno de valor: escribe una función que le pases un año
y regrese el siglo en el que está ese año (requiere investigar el
operador módulo %)

"""



def siglo(a):
    r = int(a/100)+1
    print(f'Siglo es {r}')

siglo(1984)
siglo(1702)
siglo(1000)
siglo(100)
siglo(2139)
