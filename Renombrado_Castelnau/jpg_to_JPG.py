import os

# Directorio donde se encuentran las imágenes .jpg
directorio = r'C:\Users\chris\AEROTOOLS-UAV Dropbox\AEROTOOLS-UAV\Datos_para_organizar\2024_02_20_SOTRESGUDO_NUMEROS_SERIE_JONATHAN\RGB\PB1\PB1_V1\Tracker3_Fila1'

# Obtener la lista de archivos en el directorio
archivos = os.listdir(directorio)

# Iterar sobre los archivos en el directorio
for archivo in archivos:
    # Verificar si el archivo es una imagen .jpg
    if archivo.endswith('.jpg'):
        # Construir la nueva ruta con la extensión .JPG
        nueva_ruta = os.path.join(directorio, archivo[:-4] + '.JPG')
        # Renombrar el archivo
        os.rename(os.path.join(directorio, archivo), nueva_ruta)
        print(f"Se ha cambiado el nombre de {archivo} a {archivo[:-4] + '.JPG'}")
