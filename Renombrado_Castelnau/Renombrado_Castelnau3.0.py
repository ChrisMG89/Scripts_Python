import json
import os
import shutil
import csv
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import re
import exifread
import customtkinter

def obtener_coordenadas_gps(imagen_path):
    with open(imagen_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="GPS GPSLongitudeRef")
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            latitud = tags['GPS GPSLatitude'].values
            longitud = tags['GPS GPSLongitude'].values
            lat_ref = tags['GPS GPSLatitudeRef'].values
            long_ref = tags['GPS GPSLongitudeRef'].values
            return latitud, longitud, lat_ref, long_ref
    return None, None, None, None

def obtener_fecha(nombre_original):
    try:
        # Expresión regular para el formato YYYYMMDD_HHMMSS
        regex_yyyymmdd_hhmmss = r'(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})'

        # Expresión regular para el formato DJI_YYYYMMDDHHMMSS
        regex_dji_yyyymmddhhmmss = r'DJI_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})'

        # Intentar hacer coincidir con el formato YYYYMMDD_HHMMSS
        match_yyyymmdd_hhmmss = re.match(regex_yyyymmdd_hhmmss, nombre_original)

        if match_yyyymmdd_hhmmss:
            # Extraer la fecha y la hora
            year, month, day, hour, minute, second = match_yyyymmdd_hhmmss.groups()
            fecha_hora = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        else:
            # Intentar hacer coincidir con el formato DJI_YYYYMMDDHHMMSS
            match_dji_yyyymmddhhmmss = re.match(regex_dji_yyyymmddhhmmss, nombre_original)
            if match_dji_yyyymmddhhmmss:
                # Extraer la fecha y la hora
                year, month, day, hour, minute, second = match_dji_yyyymmddhhmmss.groups()
                fecha_hora = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            else:
                raise ValueError("Formato de fecha no reconocido")

        # Formatear la fecha y la hora
        return fecha_hora.strftime('%Y%m%d%H%M%S')
    except ValueError as e:
        print(f"No se pudo convertir la fecha en el nombre original '{nombre_original}'. Se utilizará la fecha actual.")
        return datetime.now().strftime('%y%m%d%H%M%S')

def obtener_valor():
    mesa = combo_mesa.get()

    if mesa and directorio_originales.get():
        directorio_raiz = directorio_originales.get()
        subdirectorios = [os.path.join(directorio_raiz, d) for d in os.listdir(directorio_raiz) if os.path.isdir(os.path.join(directorio_raiz, d))]
        
        for subdirectorio in subdirectorios:
            pergola_volada, fila = obtener_pergola_volada(subdirectorio)
            print("Pergola volada:", pergola_volada)
            print("Fila:", fila)  # Agregamos estas líneas de impresión para depurar
            if pergola_volada:
                valor = inversores[pergola_volada][mesa]
                resultado_texto = f"El valor en la mesa '{mesa}' es: {valor}\n"
                resultado_label.configure(text=resultado_texto)
                
                renombrar_carpetas(pergola_volada, fila, subdirectorio)
            else:
                resultado_label.configure(text="No se encontró la pergola para la mesa seleccionada.")
    else:
        resultado_label.configure(text="Asegúrate de completar todos los campos.")

def obtener_pergola_volada(directorio):
    partes_directorio = directorio.split(os.sep)
    pergola_volada = None
    fila = None
    for parte in partes_directorio:
        match_pergola = re.match(r'([A-Za-z]+\d+)', parte)
        # Dividir la parte del directorio utilizando el guión bajo como separador
        partes = parte.split('_')
        if len(partes) == 2:
            fila = partes[1][1:]
        if match_pergola:
            posible_pergola = match_pergola.group(1)
            if posible_pergola in inversores:
                pergola_volada = posible_pergola
  
    print("Parte del directorio:", parte)
    print("Fila:", fila)
    return pergola_volada, fila


def seleccionar_directorio():
    directorio = filedialog.askdirectory(title="Seleccionar directorio de imágenes originales")
    if directorio:
        directorio_originales.set(directorio)

def renombrar_carpetas(pergola_volada, fila, directorio_originales):
    if pergola_volada not in inversores:
        print(f"Pergola '{pergola_volada}' no encontrada en el JSON.")
        return

    mesa_seleccionada = combo_mesa.get()
    indice_mesa_seleccionada = columnas.index(mesa_seleccionada)
    mesas = columnas[indice_mesa_seleccionada::-1]

    contador_imagenes = 0

    for mesa in mesas:
        valor_mesa = inversores[pergola_volada][mesa]

        if valor_mesa <= 0:
            mensaje_label.configure(text=f"No hay imágenes para la pergola '{pergola_volada}', mesa '{mesa}'.")
            continue

        directorio_destino_por_mesa = os.path.join(directorio_originales, f"{pergola_volada}_{mesa}")
        os.makedirs(directorio_destino_por_mesa, exist_ok=True)

        archivos = [archivo for archivo in os.listdir(directorio_originales) if os.path.isfile(os.path.join(directorio_originales, archivo))]
        imagenes = [archivo for archivo in archivos if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))]

        cantidad_imagenes = min(valor_mesa, len(imagenes) - contador_imagenes)
        
        nombre_carpeta_destino = os.path.basename(directorio_destino_por_mesa)

        csv_path = os.path.join(directorio_destino_por_mesa, f"{nombre_carpeta_destino}_F{fila}.csv")
        with open(csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            contador_columnas = 1

            for i in range(contador_imagenes, contador_imagenes + cantidad_imagenes):
                fecha_original = obtener_fecha(imagenes[i])

                nuevo_nombre_base = f"{pergola_volada}_{mesa}"
                nuevo_nombre = f"{fecha_original}_{nuevo_nombre_base}-F{fila}-C{contador_columnas}"

                viejo_ruta = os.path.join(directorio_originales, imagenes[i])
                nuevo_ruta = os.path.join(directorio_destino_por_mesa, f"{nuevo_nombre}{os.path.splitext(imagenes[i])[1]}")

                shutil.copy(viejo_ruta, nuevo_ruta)

                latitud, longitud, lat_ref, long_ref = obtener_coordenadas_gps(viejo_ruta)
                latitud_decimal = float(latitud[0]) + float(latitud[1])/60 + float(latitud[2])/3600
                longitud_decimal = float(longitud[0]) + float(longitud[1])/60 + float(longitud[2])/3600

                if lat_ref == 'S':
                    latitud_decimal *= -1
                if long_ref == 'W':
                    longitud_decimal *= -1

                csv_writer.writerow([f"{nuevo_nombre}{os.path.splitext(imagenes[i])[1]}", latitud_decimal, longitud_decimal])

                print(f"Se ha renombrado y copiado {imagenes[i]} para la pergola '{pergola_volada}', mesa '{mesa}' a '{directorio_destino_por_mesa}' con este renombrado '{nuevo_nombre}'.")

                contador_columnas += 1

        contador_imagenes += cantidad_imagenes

        print(f"Se ha creado el archivo CSV en: {csv_path}")

with open('castelnau.json', 'r') as json_file:
    inversores = json.load(json_file)

root = customtkinter.CTk()
root.title("Obtener Valor y Renombrar Carpetas")
root.iconbitmap(default='atom.ico')

directorio_originales = tk.StringVar()

label_directorio = customtkinter.CTkLabel(root, text="Directorio:")
entry_directorio = customtkinter.CTkEntry(root, state="readonly", textvariable=directorio_originales)
button_seleccionar_directorio = customtkinter.CTkButton(root, fg_color="#EE763C", text="Seleccionar Directorio", command=seleccionar_directorio)

label_mesa = customtkinter.CTkLabel(root, text="Mesa:")
columnas = ["A", "B", "C", "D", "E"]
combo_mesa = ttk.Combobox(root, values=columnas)

button_obtener_valor = customtkinter.CTkButton(root, fg_color="#EE763C", text="Renombrar", command=obtener_valor)
resultado_label = customtkinter.CTkLabel(root, text="")

mensaje_label = customtkinter.CTkLabel(root, text="")

label_directorio.grid(row=0, column=0, padx=5, pady=5)
entry_directorio.grid(row=0, column=1, padx=5, pady=5)
button_seleccionar_directorio.grid(row=0, column=2, padx=5, pady=5)
label_mesa.grid(row=1, column=0, padx=5, pady=5)
combo_mesa.grid(row=1, column=1, padx=5, pady=5)
button_obtener_valor.grid(row=3, column=1, padx=5, pady=10)
resultado_label.grid(row=4, column=0, columnspan=2, pady=5)
mensaje_label.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
