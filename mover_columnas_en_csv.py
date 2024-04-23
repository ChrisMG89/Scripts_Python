"""
Script para mover datos de ciertas columnas a otras en un archivo CSV de datos técnicos de una planta.
Realiza las siguientes operaciones:
- Lee un archivo CSV con datos técnicos de una planta.
- Mueve datos de la columna ESTRUCTURA_TRACKER a la columna PITCH.
- Mueve datos de la columna TIPOLOGIA a la columna LONG_MAX_MESA.
- Rellena las columnas originales con ceros.
- Guarda el resultado en un nuevo archivo CSV.
"""

import pandas as pd

# Leer el archivo CSV
df = pd.read_csv("DATOS_TECNICOS_PLANTA - copia.csv", sep=";")

# Mover datos de ESTRUCTURA_TRACKER a PITCH
df['PITCH'] = df['ESTRUCTURA_TRACKER']
df['ESTRUCTURA_TRACKER'] = 0  # Rellenar ESTRUCTURA_TRACKER con 0

# Mover datos de TIPOLOGIA a LONG_MAX_MESA
df['LONG_MAX_MESA'] = df['TIPOLOGIA']
df['TIPOLOGIA'] = 0  # Rellenar TIPOLOGIA con 0

# Guardar el DataFrame resultante en un nuevo archivo CSV
df.to_csv("archivo_actualizado.csv", sep=";", index=False)

print("¡Proceso completado! Se han movido los datos y rellenado las columnas según sea necesario.")
