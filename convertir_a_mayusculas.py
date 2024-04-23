"""
Script para convertir todas las palabras en un archivo CSV a mayúsculas.
Realiza las siguientes operaciones:
- Lee un archivo CSV sin procesar.
- Convierte todas las palabras a mayúsculas.
- Guarda el resultado en un nuevo archivo CSV.
"""

import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("archivo_sin_columnas.csv", sep=";")

# Convertir todas las palabras a mayúsculas
df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv("tu_archivo_mayusculas.csv", sep=";", index=False)

print("¡Proceso completado! Se han convertido todas las palabras a mayúsculas y se ha guardado el archivo en 'tu_archivo_mayusculas.csv'.")
