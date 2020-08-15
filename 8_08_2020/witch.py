"""
Existe una bruja que debe combinar una pocion
La pocion toma tres ingredientes, las raices cyan, los ojos magenta y las plumas amarrilla y
lenguas negras
De acuerdo a la cantida dde cada uno, se genera una poción distinta. Al final todos los
elementos ya liquidos se suman para dar tanto una cantidad de líquido total como un color.
La maxima cantida d de liquido por cada uno que ademas es su concentracion de color son
255 ml.
El usuario dara la entrada en terminos de porcentajes 0 a 100%
Expresa el resultado tanto de ml como de color.
"""
def user_input(text):
    a = int(input(text))/100*255
    return a
ing_c =  user_input('% de raices cyan')
ing_m = user_input('% de ojos magenta')
ing_y = user_input('% de plumas amarilla')
ing_k = user_input('% de plumas nregras')
ml = ing_c + ing_m + ing_y + ing_k
ln = f'Tu forma tiene c:{ing_c} m:{ing_m} y:{ing_y} k:{ing_y} con ML: {ml}'
print(ln)
