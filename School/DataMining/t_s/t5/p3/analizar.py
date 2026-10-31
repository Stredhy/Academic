import csv

edades = []

# Leer el archivo generado por R
with open("resultado.csv", "r") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        edades.append(int(fila["edad"]))

# Calcular un pequeño resumen
promedio = sum(edades) / len(edades)

print("Edades:", edades)
print("Edad promedio:", promedio)
