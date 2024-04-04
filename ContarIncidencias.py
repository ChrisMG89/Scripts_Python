import os
import pandas as pd

# Obtener la ruta del directorio actual del script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Lista de archivos CSV con rutas absolutas
archivos = [
    os.path.join(dir_path, 'ruta/del/directorio/con/los/csv', 'GARCIA_SARA_HUEDO_PB1_V1.csv'),
    os.path.join(dir_path, 'ruta/del/directorio/con/los/csv', 'GARCIA_SARA_HUEDO_PB1_V2.csv'),
    # Agrega las rutas absolutas para los demás archivos
]

# Lista para almacenar los DataFrames
dataframes = []

# Leer los archivos CSV y manejo de errores
for archivo in archivos:
    try:
        df = pd.read_csv(archivo)
        dataframes.append(df)
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo {archivo} está vacío o no es un archivo CSV válido.")
    except pd.errors.ParserError:
        print(f"Error: Problema al leer el archivo {archivo}. Verifica el formato del archivo.")

# Concatenar los DataFrames
merged_df = pd.concat(dataframes, ignore_index=True)

# Guardar el DataFrame concatenado en un nuevo archivo CSV
merged_df.to_csv(os.path.join(dir_path, 'merged_files.csv'), index=False)
