"""
Script para fusionar tres archivos CSV basados en un identificador único y guardar el resultado en un nuevo archivo.
Realiza las siguientes operaciones:
- Lee tres archivos CSV diferentes.
- Convierte la columna EPSG del segundo archivo en tipo "object".
- Fusiona los tres DataFrames en uno solo basado en el identificador único "ID_PLANTA".
- Guarda el DataFrame combinado en un nuevo archivo CSV.
"""


import pandas as pd

# Leer los tres archivos CSV
df1 = pd.read_csv("tu_archivo_mayusculas.csv", sep=";")
df2 = pd.read_csv("DATOS_TECNICOS_PLANTA.csv", sep=";", dtype={"epsg": object})  # Convertir la columna EPSG en "object"
#df3 = pd.read_csv("datos_tecnicos.csv", sep=";")

# Fusionar los tres DataFrames en uno solo basado en el identificador único "planta"
df_combinado = pd.merge(df1, df2, on="ID_PLANTA", how="outer")
#df_combinado = pd.merge(df_combinado, df3, on="planta", how="outer")

# Guardar el DataFrame resultante en un nuevo archivo CSV
df_combinado.to_csv("datos_combinados.csv", sep=";", index=False)
print(df_combinado)

print("¡Proceso completado! Los datos combinados se han guardado en 'datos_combinados.csv'.")
