"""
Script para procesar un archivo CSV de datos técnicos de una planta.
Realiza las siguientes operaciones:
- Convierte nombres de columnas a mayúsculas.
- Reemplaza los valores faltantes con ceros o nulos según sea necesario.
Guarda el resultado en un nuevo archivo CSV.
"""


import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("DATOS_TECNICOS_PLANTA.csv", sep=";")

# Convertir los nombres de las columnas a mayúsculas
df.columns = df.columns.str.upper()

# Iterar sobre cada columna
for columna in df.columns:
    # Verificar si la columna es EPSG
    if columna == "EPSG":
        # Convertir la columna EPSG a tipo de datos "object"
        df["EPSG"] = df["EPSG"].astype(str)

    # Verificar si hay valores faltantes en la columna
    if df[columna].isnull().any():
        # Si hay valores faltantes, reemplazarlos con ceros (0)
        df[columna].fillna(0, inplace=True)  # O puedes usar df[columna].fillna(None, inplace=True) para reemplazarlos con nulos

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv("archivo_actualizado.csv", sep=";", index=False)

print("¡Proceso completado! Se han reemplazado los valores faltantes con ceros o nulos según sea necesario.")
