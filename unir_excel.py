'''------------------------------------------------------------------------------------
Nombre : Combinar Archivos Excel desde una Carpeta
Readme : 
    Este script de Python facilita la combinación de múltiples archivos Excel ubicados en una carpeta específica en un solo archivo Excel. Utiliza la biblioteca pandas para cargar y manipular los datos de los archivos Excel.

Requisitos: 
    Python 3.x
    Bibliotecas Python: pandas, tkinter

Uso:
    Ejecuta el script Python.
    Haz clic en el botón "Seleccionar Carpeta" para elegir la carpeta que contiene los archivos Excel que deseas combinar.
    Haz clic en el botón "Seleccionar Directorio" para elegir el directorio donde se guardará el nuevo archivo Excel combinado.
    Haz clic en el botón "Combinar Excel" para iniciar el proceso de combinación de archivos Excel.
    Una vez completado, se mostrará un mensaje indicando el éxito de la combinación y la ubicación del archivo combinado.

Notas:
    Los archivos Excel deben tener la extensión .xlsx.
    Los archivos Excel deben contener datos que tengan un formato consistente para una combinación efectiva.
    Asegúrate de tener suficiente espacio en disco para almacenar el archivo Excel combinado, especialmente si los archivos de origen son grandes.
    Se recomienda realizar una copia de seguridad de los archivos de origen antes de realizar la combinación.
    Si se desea personalizar la lógica de combinación o la interfaz de usuario, el código puede ser modificado según las necesidades específicas.

    
    
¡Espero que encuentres útil este script para combinar archivos Excel de manera eficiente! Si necesitas ayuda adicional, no dudes en preguntar.

------------------------------------------------------------------------------------'''


import os
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("blue")

def seleccionar_carpeta():
    # Pedir al usuario que seleccione la carpeta que contiene los archivos Excel de entrada
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de archivos Excel")
    if carpeta:
        carpeta_entrada.set(carpeta)

def seleccionar_directorio_salida():
    # Pedir al usuario que seleccione el directorio de salida para el nuevo archivo Excel
    directorio = filedialog.askdirectory(title="Seleccionar directorio de salida")
    if directorio:
        directorio_salida.set(directorio)

def combinar_excel():
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
    archivo_salida = os.path.join(directorio, f"{nombre_carpeta}.xlsx")

    # Crear una lista para almacenar todos los datos de los archivos Excel
    datos_combinados = []

    # Función auxiliar para buscar archivos Excel de manera recursiva en una carpeta
    def buscar_excel(carpeta):
        for root, _, files in os.walk(carpeta):
            for archivo in files:
                if archivo.lower().endswith('.xlsx') and "snor_results" in archivo.lower() and "original" not in archivo.lower():
                    archivo_excel = os.path.join(root, archivo)
                    print(f"Uniendo archivo: {archivo_excel}")
                    df = pd.read_excel(archivo_excel)
                    datos_combinados.append(df)

    # Buscar archivos Excel en la carpeta de entrada de manera recursiva
    buscar_excel(carpeta)

    # Combinar todos los datos en un solo DataFrame
    datos_combinados = pd.concat(datos_combinados)

    # Guardar el DataFrame combinado en un archivo Excel de salida
    datos_combinados.to_excel(archivo_salida, index=False)

    resultado_label.config(text=f"Se han combinado exitosamente los archivos Excel en '{archivo_salida}'.")

# Crear la interfaz
root = customtkinter.CTk()
root.title("Combinar Archivos Excel")

# Variables para almacenar la carpeta de entrada y el directorio de salida
carpeta_entrada = tk.StringVar()
directorio_salida = tk.StringVar()

# Widgets
label_carpeta = customtkinter.CTkLabel(root, text="Carpeta de entrada:")
entry_carpeta = customtkinter.CTkEntry(root, textvariable=carpeta_entrada, state="readonly")
button_seleccionar_carpeta = customtkinter.CTkButton(root, fg_color="#EE763C", text="Seleccionar Carpeta", command=seleccionar_carpeta)

label_directorio = customtkinter.CTkLabel(root, text="Directorio de salida:")
entry_directorio = customtkinter.CTkEntry(root, textvariable=directorio_salida, state="readonly")
button_seleccionar_directorio = customtkinter.CTkButton(root, fg_color="#EE763C" ,text="Seleccionar Directorio", command=seleccionar_directorio_salida)

button_combinar = customtkinter.CTkButton(root, fg_color="#EE763C", text="Combinar Excel", command=combinar_excel)
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

resultado_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Iniciar la interfaz
root.mainloop()
