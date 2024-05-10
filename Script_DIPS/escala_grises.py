import os
from PIL import Image

# Carpeta que contiene las imágenes TIFF
folder_path = r"C:\Users\chris\Desktop\Pruebas de rango\PB1_V1\TIFF"

# Carpeta para las imágenes con la nueva paleta de colores
output_folder = os.path.join(folder_path, "Imagenes_Con_Paleta_Gris")
os.makedirs(output_folder, exist_ok=True)

# Lista de valores de intensidad de grises
gray_scale_values = list(range(20, 180))  # Escala de grises de 40 a 200

# Crear una paleta de grises personalizada
gray_palette = [i for i in gray_scale_values] * 3  # Replicar la lista de valores de grises para los canales RGB

# Iterar sobre todas las imágenes TIFF en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".tiff") or filename.endswith(".tif"):
        # Abrir la imagen térmica
        image_path = os.path.join(folder_path, filename)
        thermal_image = Image.open(image_path)

        # Convertir la imagen a escala de grises
        thermal_image_gray = thermal_image.convert("L")

        # Establecer la paleta de grises personalizada
        thermal_image_gray.putpalette(gray_palette)

        # Guardar la imagen en escala de grises en la carpeta de salida
        output_image_path = os.path.join(output_folder, filename)
        thermal_image_gray.save(output_image_path)
