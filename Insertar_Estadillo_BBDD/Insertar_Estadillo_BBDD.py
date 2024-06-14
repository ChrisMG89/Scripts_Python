import csv
import psycopg2
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

class EstadilloUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargar Estadillo CSV")

        self.file_label = ctk.CTkLabel(root, text="Archivo CSV: ")
        self.file_label.grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.file_entry = ctk.CTkEntry(root, width=300)
        self.file_entry.grid(row=0, column=1, pady=5, padx=5)

        self.browse_button = ctk.CTkButton(root, text="Buscar", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, pady=5, padx=5)

        self.upload_button = ctk.CTkButton(root, text="Cargar", command=self.cargar_estadillo)
        self.upload_button.grid(row=1, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file_entry.insert(0, file_path)

    def cargar_estadillo(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return

        # Conexión a la base de datos
        try:
            conn = psycopg2.connect(
                dbname='christiandb',
                user='atom',
                password='Maps2019!',
                host='82.223.110.207',
                port='5432'
            )
            cursor = conn.cursor()

            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';', skipinitialspace=True)
                
                for row in reader:
                    empresa = row.get('Empresa', '')
                    trabajo = row.get('Trabajo', '')
                    fecha_str = row.get('Fecha', '')
                    if fecha_str:
                        fecha = datetime.strptime(fecha_str, '%Y:%m:%d').date()
                    else:
                        fecha = None
                    
                    piloto = row.get('Piloto', '')
                    equipo = row.get('Equipo_de_vuelo', '')
                    hora_inicio_str = row.get('Hora_de_inicio', '')
                    if hora_inicio_str:
                        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M:%S').time()
                    else:
                        hora_inicio = None
                    
                    hora_final_str = row.get('Hora_final', '')
                    if hora_final_str:
                        hora_final = datetime.strptime(hora_final_str, '%H:%M:%S').time()
                    else:
                        hora_final = None
                    
                    pb = row.get('PB', '')
                    vuelo = int(row.get('Vuelo', 0))

                    if fecha:
                        cursor.execute("""
                            INSERT INTO Estadillos (Empresa, Trabajo, Fecha, Piloto, Equipo_de_vuelo, Hora_de_inicio, Hora_final, PB, Vuelo)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (empresa, trabajo, fecha, piloto, equipo, hora_inicio, hora_final, pb, vuelo))
                
                conn.commit()
                messagebox.showinfo("Éxito", "Datos cargados correctamente")

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al cargar los datos: {error}")

        finally:
            if conn:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = EstadilloUploaderApp(root)
    root.mainloop()
