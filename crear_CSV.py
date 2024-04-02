'''------------------------------------------------------------------------------
Nombre : Generador de CSV de Coordenadas GPS

Readme:
    Este script de Python permite generar un archivo CSV que contiene las coordenadas GPS (latitud y longitud) de las imágenes en una carpeta seleccionada. 
    Utiliza la biblioteca exifread para leer los metadatos de las imágenes y la biblioteca tkinter para crear una interfaz gráfica de usuario simple.
Requisitos:
    -Python 3.x
    -Biblioteca exifread (instalable a través de pip install exifread)

                                    pip install install exifread
Uso:
    Ejecuta el script Python.
    Haz clic en el botón "Buscar" para seleccionar la carpeta que contiene las imágenes de las cuales deseas extraer las coordenadas GPS.
    Haz clic en el botón "Generar CSV" para iniciar el proceso de generación del archivo CSV.
    Una vez completado, se mostrará un mensaje de éxito que indica el nombre del archivo CSV generado y su ubicación.

Notas:
    Asegúrate de tener instalada la biblioteca exifread. Puedes instalarla usando pip install exifread.
    El script buscará las coordenadas GPS en los metadatos de las imágenes (si están disponibles).
    El archivo CSV generado contendrá tres columnas: nombre del archivo de imagen, latitud y longitud.
    Si una imagen no contiene coordenadas GPS, no se incluirá en el archivo CSV.
    Si deseas personalizar el formato o la lógica del script, puedes modificarlo según tus necesidades específicas.
    Se recomienda realizar una copia de seguridad de las imágenes antes de ejecutar el script, ya que el proceso puede modificar los archivos en la carpeta seleccionada.
----------------------------------------------------------------------------'''


import os
import exifread
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("green")

def get_decimal_coords(tag):
    degrees = tag.values[0].num
    minutes = tag.values[1].num
    seconds = tag.values[2].num / tag.values[2].den
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    return decimal_degrees

def obtener_coordenadas_gps(imagen_path):
    with open(imagen_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="GPS GPSLongitudeRef")
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            latitud = get_decimal_coords(tags['GPS GPSLatitude'])
            longitud = get_decimal_coords(tags['GPS GPSLongitude'])
            lat_ref = str(tags['GPS GPSLatitudeRef'])
            long_ref = str(tags['GPS GPSLongitudeRef'])
            if lat_ref == 'S':
                latitud = -latitud
            if long_ref == 'W':
                longitud = -longitud
            return latitud, longitud
    return None, None

def generate_csv(folder_path):
    files = os.listdir(folder_path)
    output_csv = os.path.join(folder_path, os.path.basename(folder_path) + '.csv')
    with open(output_csv, 'w', newline='') as csvfile:
        import csv
        writer = csv.writer(csvfile, delimiter=',')
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            lat, lon = obtener_coordenadas_gps(filepath)
            if lat is not None and lon is not None:
                writer.writerow([filename, lat, lon])
    success_message = f'¡CSV generado exitosamente! Nombre del archivo: {os.path.basename(output_csv)}'
    messagebox.showinfo("Éxito", success_message)

def browse_folder():
    folder_path = filedialog.askdirectory(title='Selecciona la carpeta con los archivos')
    folder_entry.delete(0, 'end')
    folder_entry.insert(0, folder_path)

def run_script():
    folder_path = folder_entry.get()
    if folder_path:
        generate_csv(folder_path)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta.")

# Configuración de la ventana
root = customtkinter.CTk()
root.title("Generador de CSV de Coordenadas GPS")

# Etiqueta y entrada para el directorio
folder_label = customtkinter.CTkLabel(root, text="Selecciona la carpeta con los archivos:")
folder_label.grid(row=0, column=0, padx=5, pady=5)
folder_entry = customtkinter.CTkEntry(root, width=150)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
browse_button = customtkinter.CTkButton(root, fg_color="#EE763C", text="Buscar", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Botón para ejecutar el script
run_button = customtkinter.CTkButton(root, fg_color="#EE763C", text="Generar CSV", command=run_script)
run_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
