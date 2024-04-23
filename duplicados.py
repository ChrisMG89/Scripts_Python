"""
Script para eliminar duplicados de un archivo CSV de datos de plantas planificadas.
Realiza las siguientes operaciones:
- Lee un archivo CSV de datos de plantas planificadas.
- Elimina los registros duplicados basados en el identificador único "planta".
- Guarda el resultado en un nuevo archivo CSV sin duplicados.
"""


import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("datos_plantas_planif.csv", sep=";")

# Eliminar duplicados basados en el identificador único "planta"
df_sin_duplicados = df.drop_duplicates(subset="planta")

# Guardar el DataFrame resultante en un nuevo archivo CSV
df_sin_duplicados.to_csv("archivo_sin_duplicados.csv", sep=";", index=False)

print("¡Proceso completado! Los duplicados han sido eliminados y el archivo resultante se ha guardado en 'archivo_sin_duplicados.csv'.")
