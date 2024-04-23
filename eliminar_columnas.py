"""
Script para eliminar columnas especificadas de un archivo CSV.
Realiza las siguientes operaciones:
- Lee un archivo CSV.
- Elimina las columnas especificadas en la lista 'columnas_a_eliminar'.
- Guarda el resultado en un nuevo archivo CSV sin las columnas eliminadas.
"""



import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("HOLA.csv", sep=";")

# Eliminar las columnas especificadas
columnas_a_eliminar = ["Provincia"]  # Lista de nombres de columnas a eliminar
df = df.drop(columns=columnas_a_eliminar)

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv("archivo_sin_columnas.csv", sep=";", index=False)

print("¡Proceso completado! Las columnas han sido eliminadas y el archivo")
