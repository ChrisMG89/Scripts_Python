import os
from shutil import copyfile
import pandas as pd
import re
import sys

# Obtener valores de los campos de entrada desde los argumentos de la línea de comandos
directorio_raiz = sys.argv[1].replace("\\", "/")
ruta_csv = sys.argv[2].replace("\\", "/")
PB = sys.argv[3]
vuelo = sys.argv[4]

try:
    # Operaciones en la carpeta de imágenes térmicas
    ruta_img_termica = os.path.join(directorio_raiz, "TERMICA", f"PB{PB}/PB{PB}_V{vuelo}")
    print(f"Ruta Imágenes Térmicas: {ruta_img_termica}")
    archivos_termica = os.listdir(ruta_img_termica)

    # Buscar cualquier archivo CSV que contenga los valores de PB y vuelo en su nombre
    pattern_termica = re.compile(f".*PB{PB}_V{vuelo}.*\\.csv")
    archivos_csv_termica = [archivo for archivo in os.listdir(ruta_csv) if pattern_termica.match(archivo)]

    if archivos_csv_termica:
        archivo_csv_termica = archivos_csv_termica[0]  # Tomar el primer archivo encontrado
        print(f"Archivo CSV térmico encontrado: {archivo_csv_termica}")

        insp_termica = pd.read_csv(os.path.join(ruta_csv, archivo_csv_termica))
        archivos_sel_termica = insp_termica.loc[insp_termica['imagen_t'].isin(archivos_termica), 'imagen_t']

        ruta_seleccion_termica = os.path.join(ruta_img_termica, "Seleccion_ATOM")
        os.makedirs(ruta_seleccion_termica, exist_ok=True)

        for archivo in archivos_sel_termica:
            origen = os.path.join(ruta_img_termica, archivo)
            destino = os.path.join(ruta_seleccion_termica, archivo)
            copyfile(origen, destino)

    # Operaciones en la carpeta de imágenes RGB
    ruta_img_rgb = os.path.join(directorio_raiz, "RGB", f"PB{PB}/PB{PB}_V{vuelo}")
    print(f"Ruta Imágenes RGB: {ruta_img_rgb}")
    archivos_rgb = os.listdir(ruta_img_rgb)

    # Buscar cualquier archivo CSV que contenga los valores de PB y vuelo en su nombre
    pattern_rgb = re.compile(f".*PB{PB}_V{vuelo}.*\\.csv")
    archivos_csv_rgb = [archivo for archivo in os.listdir(ruta_csv) if pattern_rgb.match(archivo)]

    if archivos_csv_rgb:
        archivo_csv_rgb = archivos_csv_rgb[0]  # Tomar el primer archivo encontrado
        print(f"Archivo CSV RGB encontrado: {archivo_csv_rgb}")

        insp_rgb = pd.read_csv(os.path.join(ruta_csv, archivo_csv_rgb))
        archivos_sel_rgb = insp_rgb.loc[insp_rgb['imagen_rgb'].isin(archivos_rgb), 'imagen_rgb']

        ruta_seleccion_rgb = os.path.join(ruta_img_rgb, "Seleccion_ATOM")
        os.makedirs(ruta_seleccion_rgb, exist_ok=True)

        for archivo in archivos_sel_rgb:
            origen = os.path.join(ruta_img_rgb, archivo)
            destino = os.path.join(ruta_seleccion_rgb, archivo)
            copyfile(origen, destino)

    # Mostrar número de imágenes copiadas y mensaje de éxito
    num_imagenes_copiadas_termica = archivos_sel_termica.nunique() if archivos_csv_termica else 0
    num_imagenes_copiadas_rgb = archivos_sel_rgb.nunique() if archivos_csv_rgb else 0
    mensaje_exito = f"Operaciones ejecutadas con éxito. Número de imágenes copiadas: {num_imagenes_copiadas_termica} de térmicas y {num_imagenes_copiadas_rgb} de RGB."

    print(mensaje_exito)

except Exception as e:
    # Mostrar error en la caja de texto y en mensaje de error
    print(f"Error: {e}")
    sys.exit(1)
