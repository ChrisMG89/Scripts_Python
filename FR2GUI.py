import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("blue")

def process_files():
    # Función para procesar los archivos
    
    # Verificar si se han cargado los archivos
    if FR_file_path == "" or comparison_file_path == "":
        messagebox.showerror("Error", "Por favor, primero selecciona los archivos.")
        return
    
    # Leer el archivo FlashReport
    try:
        df_fr = pd.read_excel(FR_file_path, usecols=[0], dtype=str)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo FlashReport: {str(e)}")
        return
    
    # Leer el archivo de comparación
    try:
        df_comparison = pd.read_excel(comparison_file_path, dtype={'Serial Number': str})
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de comparación: {str(e)}")
        return
    
    # Procesar el archivo de comparación
    df_comparison['ID_FR_2'] = 0
    
    # Buscar coincidencias en el archivo FlashReport
    for i in range(len(df_comparison)):
        serial_number = df_comparison['Serial Number'].iloc[i]
        coincidencias = df_fr['SN Report'].isin([serial_number])
                    
        if coincidencias.any():
            df_comparison.loc[i, 'ID_FR_2'] = 1

    # Buscar repeticiones de números de serie en el archivo
    for i in range(len(df_comparison)):
        serial_number = df_comparison['Serial Number'].iloc[i]
        repeticiones = df_comparison['Serial Number'].value_counts(dropna=False)[serial_number]
                    
        if repeticiones > 1 and df_comparison.loc[i, 'ID_FR_2'] == 1:
            df_comparison.loc[i, 'ID_FR_2'] = 2
    
    # Mostrar el recuento de valores en la columna ID_FR_2
    print("Recuento de valores en la columna ID_FR_2:")
    print(df_comparison["ID_FR_2"].value_counts())
    
    # Guardar los cambios en el mismo archivo
    try:
        df_comparison.to_excel(comparison_file_path, sheet_name='Hoja1', index=False)
        messagebox.showinfo("Éxito", "El archivo ha sido procesado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo procesado: {str(e)}")

def load_FR_file():
    global FR_file_path
    FR_file_path = filedialog.askopenfilename(title="Seleccionar FlashReport", filetypes=[("Excel files", ".xlsx"), ("All files", ".*")])
    if FR_file_path != "":
        print("Archivo FlashReport cargado:", FR_file_path)
        fr_label.config(text=f"FlashReport seleccionado: {os.path.basename(FR_file_path)}")

def load_comparison_file():
    global comparison_file_path
    comparison_file_path = filedialog.askopenfilename(title="Seleccionar archivo para comparar", filetypes=[("Excel files", ".xlsx"), ("All files", ".*")])
    if comparison_file_path != "":
        print("Archivo para comparar cargado:", comparison_file_path)
        comparison_label.config(text=f"Archivo a comparar seleccionado: {os.path.basename(comparison_file_path)}")

# Crear ventana principal
root = customtkinter.CTk()
root.title("Flash Report 2")
root.geometry("400x200")

# Crear botón para cargar el archivo FlashReport
load_FR_button = customtkinter.CTkButton(root, fg_color="#EE763C", text="Cargar FlashReport", command=load_FR_file)
load_FR_button.pack(pady=5)

# Crear etiqueta para mostrar el nombre del archivo FlashReport seleccionado
fr_label = customtkinter.CTkLabel(root, text="")
fr_label.pack()

# Crear botón para cargar el archivo de comparación
load_comparison_button = customtkinter.CTkButton(root, fg_color="#EE763C", text="Cargar Archivo para Comparar", command=load_comparison_file)
load_comparison_button.pack(pady=5)

# Crear etiqueta para mostrar el nombre del archivo de comparación seleccionado
comparison_label = customtkinter.CTkLabel(root, text="")
comparison_label.pack()

# Crear botón para iniciar el procesamiento de archivos
process_button = customtkinter.CTkButton(root, fg_color="#EE763C", text="Procesar Archivos", command=process_files)
process_button.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
