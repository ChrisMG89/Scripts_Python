import customtkinter as ctk
import psycopg2
import datetime
from tkinter import messagebox

class TiempoVueloPilotosUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiempo de Vuelo de Pilotos")

        self.label = ctk.CTkLabel(root, text="Piloto")
        self.label.grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.combo_piloto = ctk.CTkComboBox(root, values=self.obtener_lista_pilotos())
        self.combo_piloto.grid(row=0, column=1, pady=5, padx=5)

        self.button = ctk.CTkButton(root, text="Obtener Tiempo de Vuelo", command=self.obtener_tiempo_vuelo)
        self.button.grid(row=1, column=0, columnspan=2, pady=10)

        self.result_label = ctk.CTkLabel(root, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def obtener_lista_pilotos(self):
        try:
            # Conexión a la base de datos
            conn = psycopg2.connect(
                dbname='christiandb',
                user='atom',
                password='Maps2019!',
                host='82.223.110.207',
                port='5432'
            )
            cursor = conn.cursor()

            # Consulta SQL para obtener todos los pilotos
            cursor.execute("SELECT DISTINCT Piloto FROM Estadillos")
            pilotos = cursor.fetchall()

            # Cerrar la conexión y el cursor
            cursor.close()
            conn.close()

            return [piloto[0] for piloto in pilotos]

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al obtener la lista de pilotos: {error}")
            return []

    def obtener_tiempo_vuelo(self):
        piloto = self.combo_piloto.get()
        if not piloto:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un piloto")
            return

        try:
            # Conexión a la base de datos
            conn = psycopg2.connect(
                dbname='christiandb',
                user='atom',
                password='Maps2019!',
                host='82.223.110.207',
                port='5432'
            )
            cursor = conn.cursor()

            # Consulta SQL para obtener los intervalos de tiempo de vuelo para un piloto específico
            cursor.execute("""
                SELECT EXTRACT(EPOCH FROM SUM(Hora_final - Hora_de_inicio)) AS Tiempo_total_segundos
                FROM Estadillos
                WHERE Piloto = %s
            """, (piloto,))
            tiempo_total_segundos = cursor.fetchone()[0]

            if tiempo_total_segundos is None:
                tiempo_total_segundos = 0

            # Convertir los segundos a formato hh:mm:ss
            tiempo_total = datetime.timedelta(seconds=tiempo_total_segundos)
            
            # Formatear la salida de manera más legible
            total_horas, remainder = divmod(tiempo_total.total_seconds(), 3600)
            total_minutos, total_segundos = divmod(remainder, 60)
            tiempo_total_formateado = f"{int(total_horas):02}:{int(total_minutos):02}:{int(total_segundos):02}"

            self.result_label.configure(text=f"Tiempo total de vuelo para {piloto}: {tiempo_total_formateado}")

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al obtener los datos: {error}")

        finally:
            # Cerrar la conexión y el cursor
            if conn:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Puedes cambiar a "light" si prefieres
    ctk.set_default_color_theme("blue")  # Tema de color azul

    root = ctk.CTk()
    app = TiempoVueloPilotosUI(root)
    root.mainloop()
