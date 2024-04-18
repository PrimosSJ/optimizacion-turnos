filename = 'primos.csv'
salida = open('salida.txt', 'w')
file = open(filename)
cant = file.readlines()
ultima = cant[-1].strip().split(';')

salida.write(f"INSERT INTO primos_checkins.public.tracks_primo (rol, mail, name, nick, schedule) VALUES ")

for linea in cant:
    buffer = []
    linea = linea.strip().split(';')
    linea[1] = linea[1].lower()
    
    for elemento in linea:
        if not (elemento.isnumeric()):
            elemento = "'{0}'".format(elemento)
        buffer.append(elemento)
    
    salida.write(f"(")
    
    for elemento in buffer:
        if elemento == buffer[-1]:
            salida.write(f"{elemento}")
        else:
            salida.write(f"{elemento}, ")
            
    if linea == ultima:
        salida.write(f")")
    else:
        salida.write(f"), ")

salida.write(";")
salida.close()
file.close()