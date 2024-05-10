import os
from PIL import Image

# Define los colores de la paleta "RedIron" con tonos aún más oscuros
rediron_colors = [
    (0.0, '#000000'),    # Negro para temperaturas más bajas
    (0.1, '#1E1E1E'),    # Gris oscuro
    (0.3, '#321607'),    # Marrón oscuro
    (0.4, '#492D1D'),    # Marrón oscuro
    (0.5, '#604020'),    # Marrón medio
    (0.6, '#805020'),    # Marrón claro
    (0.7, '#A07030'),    # Marrón claro
    (0.8, '#C08040'),    # Marrón claro
    (0.9, '#E09050'),    # Marrón claro
    (1.0, '#FFFFFF')     # Blanco para temperaturas más altas
]

# Carpeta que contiene las imágenes TIFF
folder_path = r"ruta/a/la/carpeta"

# Carpeta para las imágenes con la nueva paleta de colores
output_folder = os.path.join(folder_path, "Imagenes_Con_Paleta")
os.makedirs(output_folder, exist_ok=True)

# Iterar sobre todas las imágenes TIFF en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".tiff") or filename.endswith(".tif"):
        # Abrir la imagen térmica
        image_path = os.path.join(folder_path, filename)
        thermal_image = Image.open(image_path)

        # Convertir la imagen a un modo compatible para aplicar la paleta de colores
        thermal_image = thermal_image.convert("P")

        # Establecer la nueva paleta de colores
        thermal_image.putpalette(sum(rediron_colors, ()))

        # Guardar la imagen con la nueva paleta de colores en la carpeta de salida
        output_image_path = os.path.join(output_folder, filename)
        thermal_image.save(output_image_path)
