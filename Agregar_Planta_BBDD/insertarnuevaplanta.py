import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox

class DatosTecnicosPlantaUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingreso de Datos Técnicos de Planta")
        
        self.labels = ['ID_PLANTA', 'POTENCIA_MW', 'PAIS', 'PROVINCIA', 'EPSG', 'LONG', 'LAT',
                       'ESTRUCTURA_TRACKER', 'TIPOLOGIA', 'PITCH', 'ANCHO_MESA', 'LONG_MAX_MESA',
                       'LONG_MIN_MESA', 'MARCA_MODULO', 'MODELO_MODULO', 'POTENCIA_MODULO', 
                       'NUMERO_PBS', 'ORIENTACION']
        self.entries = {}

        for i, label in enumerate(self.labels):
            tk.Label(root, text=label).grid(row=i, column=0)
            if label == 'ORIENTACION':
                options = ['Vertical', 'Horizontal', '']  # Añadir opción para valor nulo
                entry = ttk.Combobox(root, values=options)
            else:
                entry = tk.Entry(root)
            entry.grid(row=i, column=1)
            self.entries[label] = entry

        self.submit_button = tk.Button(root, text="Guardar", command=self.guardar_datos)
        self.submit_button.grid(row=len(self.labels), column=0, columnspan=2)

    def guardar_datos(self):
        data = {label: entry.get().upper() if label != 'ORIENTACION' else entry.get() for label, entry in self.entries.items()}  # Convertir a mayúsculas solo para campos diferentes de orientación
        
        for key, value in data.items():
            if not value:  # Si no se ingresó ningún valor, establecer como None
                data[key] = None

        try:
            # Establecer conexión con la base de datos
            conn = psycopg2.connect(
                dbname="christiandb",
                user="atom",
                password="Maps2019!",
                host="82.223.110.207",
                port="5432"
            )

            # Crear un cursor
            cursor = conn.cursor()

            # Preparar la consulta SQL para insertar los datos
            query = """INSERT INTO "DATOS_TECNICOS_PLANTA" 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            # Ejecutar la consulta SQL
            cursor.execute(query, tuple(data.values()))

            # Confirmar la transacción
            conn.commit()

            messagebox.showinfo("Éxito", "Datos guardados correctamente")

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {error}")

        finally:
            # Cerrar la conexión y el cursor
            if conn:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatosTecnicosPlantaUI(root)
    root.mainloop()
