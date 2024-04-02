'''------------------------------------------------------------------------------
Nombre : Renombrador de extensiones

Readme:
    Este script de Python renombra todas las imágenes con la extensión .jpg en un directorio específico, cambiando la extensión a .JPG. 
    Esto puede ser útil si necesitas estandarizar las extensiones de archivo de tus imágenes o corregir inconsistencias en las extensiones.
Requisitos:
    -Python 3.x

Uso:
    Especifica el directorio donde se encuentran las imágenes .jpg en la variable directorio.
    Ejecuta el script Python.
    El script buscará todas las imágenes en el directorio especificado y cambiará la extensión de archivo de .jpg a .JPG.
    Se imprimirá un mensaje indicando el cambio de nombre para cada imagen procesada.

Notas:
    Asegúrate de proporcionar la ruta completa del directorio donde se encuentran las imágenes.
    Este script modificará los nombres de los archivos en el directorio especificado. Asegúrate de hacer una copia de seguridad de tus archivos antes de ejecutar el script si es necesario.
    Si las imágenes tienen otras extensiones además de .jpg, el script no las modificará.
    Si deseas cambiar la extensión a otro valor diferente de .JPG, puedes modificar el script para adaptarlo a tus necesidades.
----------------------------------------------------------------------------'''

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
