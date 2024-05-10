"""
Organizador de Imágenes para Inspección de Paneles Solares

Este script automatiza el proceso de organización de imágenes para la inspección de paneles solares. 
Primero, lee un archivo Excel que contiene información sobre los nombres de archivo y las categorías de defectos asociadas a cada imagen. 
Luego, crea una estructura de carpetas basada en estas categorías y copia las imágenes correspondientes a cada categoría en la carpeta adecuada. 
Además, genera un informe detallado sobre la cantidad de imágenes copiadas en cada categoría y las imágenes omitidas. 
Con esta herramienta, el proceso de gestión de imágenes de inspección se simplifica y agiliza, mejorando la eficiencia del análisis de paneles solares.

"""


import os
import shutil
import pandas as pd

# Función para copiar los archivos JPG
def copiar_archivos(origen, destino):
    try:
        shutil.copy(origen, destino)
        print(f"Archivo copiado: {origen} -> {destino}")
    except Exception as e:
        print(f"No se pudo copiar el archivo {origen}: {str(e)}")

# Ruta de la carpeta raíz donde se encuentran las subcarpetas con los archivos JPG
carpeta_raiz = r"D:\AEROTOOLS-UAV Dropbox\AEROTOOLS-UAV\Proyectos\PLANTAS_PV\SONNEDIX\CASTELNAU\2024\NUMEROS_SERIE"

# Ruta de la nueva carpeta donde se guardarán los archivos JPG copiados
nueva_carpeta_raiz = r"C:\Users\Aerotools\Desktop\Inspeccion_RGB_SONNEDIX"

# Si no existe la carpeta raíz nueva, se crea
if not os.path.exists(nueva_carpeta_raiz):
    os.makedirs(nueva_carpeta_raiz)
    print(f"Creada nueva carpeta raíz: {nueva_carpeta_raiz}")

# Leer el archivo Excel
archivo_excel = r"D:\AEROTOOLS-UAV Dropbox\AEROTOOLS-UAV\Proyectos\SONNEDIX\CASTELNAU\Inspeccion_RGB_SONNEDIX\SNOR_Results_B_ORIGINAL_QM.xlsx"  # Reemplaza con la ruta a tu archivo Excel
datos_excel = pd.read_excel(archivo_excel)
print(f"Archivo Excel cargado: {archivo_excel}")

# Obtener los nombres de los archivos JPG de la columna D
nombres_archivos = datos_excel['File'].tolist()  # Reemplaza 'File' por el nombre real de la columna
print(f"Se encontraron {len(nombres_archivos)} nombres de archivo en la columna 'File'")

# Crear las carpetas para cada categoría si no existen
categorias = ['Cell framing', 'Bus-bar intercon. Corrosion', 'Delemination in cell tab',
              'Delamination', 'Snail trails', 'Broken']

for categoria in categorias:
    carpeta_categoria = os.path.join(nueva_carpeta_raiz, categoria)
    if not os.path.exists(carpeta_categoria):
        os.makedirs(carpeta_categoria)
        print(f"Creada nueva carpeta '{categoria}': {carpeta_categoria}")

# Contadores para el informe
imagenes_copiadas = {categoria: 0 for categoria in categorias}
imagenes_omitidas = 0

# Buscar y copiar los archivos JPG en las carpetas correspondientes
for nombre_archivo in nombres_archivos:
    # Obtener los valores de las columnas H, I, J, K, L y M para este archivo
    valores_categorias = datos_excel.loc[datos_excel['File'] == nombre_archivo, 
                                         ['Cell framing', 'Bus-bar intercon. Corrosion', 
                                          'Delemination in cell tab', 'Delamination', 
                                          'Snail trails', 'Broken']].values.tolist()[0]
    
    # Verificar si hay algún valor en alguna de las categorías
    if not any(valor == 1 for valor in valores_categorias):
        print(f"Archivo omitido: {nombre_archivo} (No tiene valor en ninguna categoría)")
        imagenes_omitidas += 1
        continue

    # Buscar el archivo en la carpeta raíz y sus subcarpetas
    for raiz, carpetas, archivos in os.walk(carpeta_raiz):
        for archivo in archivos:
            if archivo == nombre_archivo:
                # Copiar el archivo en las carpetas correspondientes según los valores de las categorías
                origen = os.path.join(raiz, archivo)
                
                for categoria, valor in zip(categorias, valores_categorias):
                    if valor == 1:
                        destino = os.path.join(nueva_carpeta_raiz, categoria, archivo)
                        copiar_archivos(origen, destino)
                        imagenes_copiadas[categoria] += 1

# Mostrar informe
print("\nInforme:")
print("--------")
for categoria, cantidad in imagenes_copiadas.items():
    print(f"Copiadas {cantidad} imágenes en la carpeta '{categoria}'")
print(f"Omitidas {imagenes_omitidas} imágenes")
