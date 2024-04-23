"""
Script para leer un archivo CSV de datos combinados, especificando el tipo de datos de la columna EPSG como object.
Realiza las siguientes operaciones:
- Lee un archivo CSV de datos combinados.
- Especifica el tipo de datos de la columna EPSG como objeto.
- Reordena las columnas según un nuevo orden predefinido.
- Guarda el resultado en un nuevo archivo CSV con las columnas reordenadas.
"""


import pandas as pd

# Leer el archivo CSV, especificando el tipo de datos de la columna EPSG como object
df = pd.read_csv("datos_combinados.csv", sep=";", dtype={"epsg": object})

# Reordenar las columnas
columnas_nuevas = ['planta', 'potencia', 'pais', 'provincia', 'epsg', 'long', 'lat', 'pitch', 'long_mesas']
df = df[columnas_nuevas]

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv("archivo_reordenado.csv", sep=";", index=False)

print("¡Proceso completado! El archivo ha sido reordenado y se ha guardado en 'archivo_reordenado.csv'.")
