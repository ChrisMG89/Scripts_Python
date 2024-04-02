import os
from tkinter import *
from tkinter import filedialog
import shutil

def rename_images(tracker, fila, mesa, num_modulos, directorio):
    if not os.path.exists(directorio):
        print("El directorio especificado no existe.")
        return
    
    imagenes = [f for f in os.listdir(directorio) if f.endswith('.JPG') or f.endswith('.jpg')]
    contador = 1
    
    directorio_padre = os.path.dirname(directorio)
    
    print("Renombrando imágenes...")
    for imagen in imagenes:
        fecha = imagen.split('_')[1]
        nuevo_nombre = f"{fecha}_Tracker{tracker}_M{mesa}_F{fila}_C{contador}.JPG"
        print(f"Renombrando '{imagen}' a '{nuevo_nombre}'")
        shutil.copy(os.path.join(directorio, imagen), os.path.join(directorio_padre, nuevo_nombre))
        contador += 1
        if contador > num_modulos:
            break

    print("¡Proceso completado!")

def get_directory():
    directorio = filedialog.askdirectory()
    directorio_entry.delete(0, END)
    directorio_entry.insert(0, directorio)

def iniciar_renombrado():
    tracker = tracker_entry.get()
    fila = fila_entry.get()
    mesa = mesa_entry.get()
    num_modulos = int(num_modulos_entry.get())
    directorio = directorio_entry.get()
    
    rename_images(tracker, fila, mesa, num_modulos, directorio)

# Configuración de la interfaz gráfica
root = Tk()
root.title("Renombrador de Imágenes")

tracker_label = Label(root, text="Tracker:")
tracker_label.grid(row=0, column=0, padx=5, pady=5)
tracker_entry = Entry(root)
tracker_entry.grid(row=0, column=1, padx=5, pady=5)

fila_label = Label(root, text="Fila:")
fila_label.grid(row=1, column=0, padx=5, pady=5)
fila_entry = Entry(root)
fila_entry.grid(row=1, column=1, padx=5, pady=5)

mesa_label = Label(root, text="Mesa:")
mesa_label.grid(row=2, column=0, padx=5, pady=5)
mesa_entry = Entry(root)
mesa_entry.grid(row=2, column=1, padx=5, pady=5)

num_modulos_label = Label(root, text="Número de Módulos:")
num_modulos_label.grid(row=3, column=0, padx=5, pady=5)
num_modulos_entry = Entry(root)
num_modulos_entry.grid(row=3, column=1, padx=5, pady=5)

directorio_label = Label(root, text="Directorio:")
directorio_label.grid(row=4, column=0, padx=5, pady=5)
directorio_entry = Entry(root)
directorio_entry.grid(row=4, column=1, padx=5, pady=5)
directorio_button = Button(root, text="Seleccionar Directorio", command=get_directory)
directorio_button.grid(row=4, column=2, padx=5, pady=5)

renombrar_button = Button(root, text="Renombrar Imágenes", command=iniciar_renombrado)
renombrar_button.grid(row=5, columnspan=2, padx=5, pady=5)

root.mainloop()
