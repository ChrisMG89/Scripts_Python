import psycopg2
from tkinter import messagebox, filedialog
import bcrypt
import csv
from datetime import datetime, timedelta
import customtkinter as ctk
import os

# Configuración de la aplicación
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Gestión de BBDD")
        self.geometry("900x800")
        self.iconbitmap(default='combined_icon.ico')

        tabview = ctk.CTkTabview(self)
        tabview.pack(expand=True, fill='both')

        # Crear pestañas
        tab1 = tabview.add("Insertar Nueva Planta")
        tab2 = tabview.add("Crear Nuevo Usuario")
        tab3 = tabview.add("Actualizar Contraseña")
        tab4 = tabview.add("Insertar Estadillo")
        tab5 = tabview.add("Añadir URL Inspección")
        tab6 = tabview.add("Horas de Vuelo")

        self.init_tab1(tab1)
        self.init_tab2(tab2)
        self.init_tab3(tab3)
        self.init_tab4(tab4)
        self.init_tab5(tab5)
        self.init_tab6(tab6)

    def connect_to_db(self):
        return psycopg2.connect(
            dbname="christiandb",
            user="atom",
            password="Maps2019!",
            host="82.223.110.207",
            port="5432"
        )

    def init_tab1(self, frame):
        # Insertar Nueva Planta
        labels = ['ID_PLANTA', 'POTENCIA_MW', 'PAIS', 'PROVINCIA', 'EPSG', 'LONG', 'LAT',
                  'ESTRUCTURA_TRACKER', 'TIPOLOGIA', 'PITCH', 'ANCHO_MESA', 'LONG_MAX_MESA',
                  'LONG_MIN_MESA', 'MARCA_MODULO', 'MODELO_MODULO', 'POTENCIA_MODULO', 
                  'NUMERO_PBS', 'ORIENTACION']
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(frame, text=label).grid(row=i, column=0, pady=5, padx=5, sticky='w')
            if label == 'ESTRUCTURA_TRACKER':
                options = ['SEGUIDORES 1 EJE', 'FIJOS', 'SEGUIDORES 2 EJES']  # Opciones predefinidas
                entry = ctk.CTkComboBox(frame, values=options, width=140)
                entry.configure(state="normal")  # Permitir la entrada manual
                entry.bind("<Key>", lambda e: entry.configure(state="normal"))  # Habilitar la escritura
            elif label == 'ORIENTACION':
                options = ['Vertical', 'Horizontal', '']  # Añadir opción para valor nulo
                entry = ctk.CTkComboBox(frame, values=options)
            else:
                entry = ctk.CTkEntry(frame)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label] = entry

        self.submit_button = ctk.CTkButton(frame, text="Guardar", command=self.guardar_datos)
        self.submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def guardar_datos(self):
        data = {label: entry.get().upper() if label != 'ORIENTACION' else entry.get() for label, entry in self.entries.items()}  # Convertir a mayúsculas solo para campos diferentes de orientación
        
        for key, value in data.items():
            if not value:  # Si no se ingresó ningún valor, establecer como None
                data[key] = None

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            query = """INSERT INTO "DATOS_TECNICOS_PLANTA" 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, tuple(data.values()))
            conn.commit()

            messagebox.showinfo("Éxito", "Datos guardados correctamente")
            self.clear_entries()  # Limpiar los campos de entrada después de guardar
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {error}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def clear_entries(self):
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkComboBox):
                entry.set('')
            else:
                entry.delete(0, 'end')

    def init_tab2(self, frame):
        # Crear Nuevo Usuario
        ctk.CTkLabel(frame, text="Nombre de Usuario:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = ctk.CTkEntry(frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Contraseña:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = ctk.CTkEntry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Correo Electrónico:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(frame)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Rol:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.role_var = ctk.StringVar(value="admin")
        role_dropdown = ctk.CTkOptionMenu(frame, values=["admin", "customer"], variable=self.role_var)
        role_dropdown.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Introduzca la empresa:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.company_entry = ctk.CTkEntry(frame)
        self.company_entry.grid(row=4, column=1, padx=10, pady=5)

        create_button = ctk.CTkButton(frame, text="Crear Usuario", command=self.create_user)
        create_button.grid(row=5, column=1, padx=10, pady=5)

    def create_user(self):
        user_name = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        role = self.role_var.get()
        company = self.company_entry.get()

        if not user_name or not password or not email:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (user_name, password, email, role, company)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_name, encrypted_password, email, role, company)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def init_tab3(self, frame):
        # Actualizar Contraseña
        ctk.CTkLabel(frame, text="Correo electrónico:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.email_entry_update = ctk.CTkEntry(frame)
        self.email_entry_update.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Nueva Contraseña:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.password_entry_update = ctk.CTkEntry(frame, show="*")
        self.password_entry_update.grid(row=1, column=1, padx=10, pady=5)

        update_button = ctk.CTkButton(frame, text="Actualizar Contraseña", command=self.update_password)
        update_button.grid(row=2, column=0, padx=10, pady=5)

    def update_password(self):
        email = self.email_entry_update.get()
        new_password = self.password_entry_update.get()

        if not email or not new_password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        encrypted_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE email = %s
                """,
                (encrypted_password, email)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def init_tab4(self, frame):
        # Insertar Estadillo
        ctk.CTkLabel(frame, text="Archivo CSV: ").grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.file_entry = ctk.CTkEntry(frame, width=300)
        self.file_entry.grid(row=0, column=1, pady=5, padx=5)

        browse_button = ctk.CTkButton(frame, text="Buscar", command=self.browse_file)
        browse_button.grid(row=0, column=2, pady=5, padx=5)

        upload_button = ctk.CTkButton(frame, text="Cargar", command=self.cargar_estadillo)
        upload_button.grid(row=1, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file_entry.delete(0, 'end')  # Limpiar cualquier ruta anterior
            self.file_entry.insert(0, file_path)

    def cargar_estadillo(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Seleccione un archivo CSV")
            return

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';', skipinitialspace=True)
                
                for row in reader:
                    empresa = row.get('Empresa', '')
                    trabajo = row.get('Trabajo', '')
                    fecha_str = row.get('Fecha', '')
                    fecha = datetime.strptime(fecha_str, '%Y:%m:%d').date() if fecha_str else None
                    
                    piloto = row.get('Piloto', '')
                    equipo = row.get('Equipo_de_vuelo', '')
                    hora_inicio_str = row.get('Hora_de_inicio', '')
                    hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M:%S').time() if hora_inicio_str else None
                    
                    hora_final_str = row.get('Hora_final', '')
                    hora_final = datetime.strptime(hora_final_str, '%H:%M:%S').time() if hora_final_str else None
                    
                    pb = row.get('PB', '')
                    vuelo = int(row.get('Vuelo', 0))

                    if fecha:
                        cursor.execute("""
                            INSERT INTO Estadillos (Empresa, Trabajo, Fecha, Piloto, Equipo_de_vuelo, Hora_de_inicio, Hora_final, PB, Vuelo)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (empresa, trabajo, fecha, piloto, equipo, hora_inicio, hora_final, pb, vuelo))
                
                conn.commit()
                messagebox.showinfo("Éxito", "Datos cargados correctamente")
                self.file_entry.delete(0, 'end')  # Limpiar el campo de entrada del archivo después de cargar
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Ocurrió un error al cargar los datos: {error}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def init_tab5(self, frame):
        # Añadir URL Inspección
        ctk.CTkLabel(frame, text="URL:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.url_entry = ctk.CTkEntry(frame, width=400)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Descripción:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.description_entry = ctk.CTkEntry(frame, width=400)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        save_button = ctk.CTkButton(frame, text="Guardar", command=self.save_url)
        save_button.grid(row=2, column=1, pady=10)

    def save_url(self):
        url = self.url_entry.get().strip()
        description = self.description_entry.get().strip()

        if not url or not description:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            query = """
            INSERT INTO admin_urls (url, description) 
            VALUES (%s, %s)
            """
            cursor.execute(query, (url, description))
            conn.commit()

            messagebox.showinfo("Éxito", "URL añadida correctamente.")

            # Limpiar los campos
            self.url_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la URL: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def init_tab6(self, frame):
        # Horas de Vuelo
        ctk.CTkLabel(frame, text="Piloto:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Crear combobox con valor inicial vacío
        self.pilot_combobox = ctk.CTkComboBox(frame, values=[], state="readonly")
        self.pilot_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.pilot_combobox.set("")  # Establecer texto inicial vacío

        load_button = ctk.CTkButton(frame, text="Cargar Pilotos", command=self.load_pilots)
        load_button.grid(row=0, column=2, padx=10, pady=5)

        calculate_button = ctk.CTkButton(frame, text="Calcular Horas", command=self.calculate_flight_hours)
        calculate_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.result_label = ctk.CTkLabel(frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

    def load_pilots(self):
        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT piloto FROM estadillos")
            pilots = [row[0] for row in cursor.fetchall()]

            self.pilot_combobox.configure(values=pilots)
            self.pilot_combobox.set("")  # Restablecer el texto del combobox a vacío después de cargar
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los pilotos: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def calculate_flight_hours(self):
        selected_pilot = self.pilot_combobox.get()

        if not selected_pilot:
            messagebox.showerror("Error", "Por favor, seleccione un piloto.")
            return

        try:
            conn = self.connect_to_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT hora_de_inicio, hora_final
                FROM estadillos
                WHERE piloto = %s
                """,
                (selected_pilot,)
            )
            records = cursor.fetchall()

            total_flight_time = timedelta()
            for start_time, end_time in records:
                start = datetime.combine(datetime.today(), start_time)
                end = datetime.combine(datetime.today(), end_time)
                total_flight_time += (end - start)

            hours, remainder = divmod(total_flight_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)

            self.result_label.configure(text=f"Horas totales de vuelo: {int(hours)} horas, {int(minutes)} minutos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron calcular las horas de vuelo: {str(e)}")
        finally:
            if conn:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("orange_theme.json")

    app = App()
    app.mainloop()
