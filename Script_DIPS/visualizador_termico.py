import os
import matplotlib.pyplot as plt
from PIL import Image

# Carpeta que contiene las imágenes térmicas
folder_path = r"C:\Users\chris\Desktop\Pruebas de rango\Sin normalizar valores\Imagenes_Con_Paleta_Ajustada"

# Iterar sobre todas las imágenes en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".tiff") or filename.endswith(".tif"):
        # Abrir la imagen térmica
        image_path = os.path.join(folder_path, filename)
        thermal_image = Image.open(image_path)

        # Mostrar la imagen térmica
        plt.imshow(thermal_image, cmap='hot')  # Puedes cambiar el mapa de colores aquí
        plt.colorbar(label='Temperatura (°C)')
        plt.title('Imagen térmica: ' + filename)
        plt.xlabel('Columna de píxeles')
        plt.ylabel('Fila de píxeles')
        plt.show()
