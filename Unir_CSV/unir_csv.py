'''------------------------------------------------------------------------------------
Nombre : Combinar Archivos CSV desde una Carpeta

Readme : 
    Este script de Python facilita la combinación de múltiples archivos CSV ubicados en una carpeta específica en un solo archivo CSV. 
    Utiliza las bibliotecas estándar de Python csv y tkinter para manejar los archivos CSV y crear una interfaz gráfica simple para el usuario.
Requisitos: 
    Python 3.x

Uso:
    Ejecuta el script Python.
    Haz clic en el botón "Seleccionar Carpeta" para elegir la carpeta que contiene los archivos CSV que deseas combinar.
    Haz clic en el botón "Seleccionar Directorio" para elegir el directorio donde se guardará el nuevo archivo CSV combinado.
    Haz clic en el botón "Combinar CSV" para iniciar el proceso de combinación de archivos CSV.
    Una vez completado, se mostrará un mensaje indicando el éxito de la combinación y la ubicación del archivo CSV combinado.

Notas:
    Los archivos CSV deben tener la extensión .csv.
    Asegúrate de que los archivos CSV tengan un formato consistente para una combinación efectiva.
    Si algún archivo CSV contiene encabezados y quieres mantenerlos, asegúrate de que todos los archivos tengan los mismos encabezados o ajusta el código según sea necesario.
    Se recomienda realizar una copia de seguridad de los archivos de origen antes de realizar la combinación.
    Si se desea personalizar la lógica de combinación o la interfaz de usuario, el código puede ser modificado según las necesidades específicas.

    
    
¡Espero que encuentres útil este script para combinar archivos Excel de manera eficiente! Si necesitas ayuda adicional, no dudes en preguntar.

------------------------------------------------------------------------------------'''


import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("blue")

def seleccionar_carpeta():
    # Pedir al usuario que seleccione la carpeta que contiene los archivos CSV de entrada
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de archivos CSV")
    if carpeta:
        carpeta_entrada.set(carpeta)

def seleccionar_directorio_salida():
    # Pedir al usuario que seleccione el directorio de salida para el nuevo archivo CSV
    directorio = filedialog.askdirectory(title="Seleccionar directorio de salida")
    if directorio:
        directorio_salida.set(directorio)

def combinar_csv():
    # Obtener la carpeta de entrada y el directorio de salida
    carpeta = carpeta_entrada.get()
    directorio = directorio_salida.get()

    # Verificar si se proporcionó una carpeta de entrada
    if not carpeta:
        resultado_label.config(text="No se ha seleccionado una carpeta de entrada.")
        return

    # Verificar si se proporcionó un directorio de salida
    if not directorio:
        resultado_label.config(text="No se ha seleccionado un directorio de salida.")
        return

    # Nombre del archivo de salida basado en el nombre de la carpeta de origen
    nombre_carpeta = os.path.basename(carpeta)
    archivo_salida = os.path.join(directorio, f"{nombre_carpeta}.csv")

    # Crear una lista para almacenar todos los datos de los archivos CSV
    datos_combinados = []

    # Función auxiliar para buscar archivos CSV de manera recursiva en una carpeta
    def buscar_csv(carpeta):
        for root, _, files in os.walk(carpeta):
            for archivo in files:
                if archivo.lower().endswith('.csv') and "location" not in archivo.lower():
                    archivo_csv = os.path.join(root, archivo)
                    with open(archivo_csv, mode='r', newline='') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        for fila in csv_reader:
                            datos_combinados.append(fila)

    # Buscar archivos CSV en la carpeta de entrada de manera recursiva
    buscar_csv(carpeta)

    # Escribir los datos combinados en el archivo CSV de salida
    with open(archivo_salida, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for fila in datos_combinados:
            csv_writer.writerow(fila)

    resultado_label.config(text=f"Se han combinado exitosamente los archivos CSV en '{archivo_salida}'.")

# Crear la interfaz
root = customtkinter.CTk()
root.title("Combinar Archivos CSV")
root.iconbitmap(default='atom.ico')
 

# Variables para almacenar la carpeta de entrada y el directorio de salida
carpeta_entrada = tk.StringVar()
directorio_salida = tk.StringVar()

# Widgets
label_carpeta = customtkinter.CTkLabel(root, text="Carpeta de entrada:")
entry_carpeta = ttk.Entry(root, textvariable=carpeta_entrada, state="readonly")
button_seleccionar_carpeta = customtkinter.CTkButton(root, fg_color="#EE763C", text="Seleccionar Carpeta", command=seleccionar_carpeta)

label_directorio = customtkinter.CTkLabel(root, text="Directorio de salida:")
entry_directorio = ttk.Entry(root, textvariable=directorio_salida, state="readonly")
button_seleccionar_directorio = customtkinter.CTkButton(root, fg_color="#EE763C", text="Seleccionar Directorio", command=seleccionar_directorio_salida)

button_combinar = customtkinter.CTkButton(root, fg_color="#EE763C", text="Combinar CSV", command=combinar_csv)
resultado_label = customtkinter.CTkLabel(root, text="")

# Posicionamiento de widgets
label_carpeta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_carpeta.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
button_seleccionar_carpeta.grid(row=0, column=2, padx=5, pady=5)

label_directorio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_directorio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
button_seleccionar_directorio.grid(row=1, column=2, padx=5, pady=5)

button_combinar.grid(row=2, column=0, columnspan=3, padx=5, pady=10)
resultado_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Iniciar la interfaz
root.mainloop()
