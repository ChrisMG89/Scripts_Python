import tkinter as tk
from tkinter import messagebox
import bcrypt
import psycopg2
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("blue")


# Función para encriptar la contraseña
def encrypt_password(password):
    salt = bcrypt.gensalt()  # Genera una sal
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Encripta la contraseña
    return hashed.decode('utf-8')  # Devuelve la contraseña encriptada como string

# Función para manejar el evento de clic en el botón "Crear Usuario"
def create_user():
    # Obtener los datos del usuario desde los campos de entrada
    user_name = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    role = role_var.get()
    company = company_entry.get()

    # Verificar que se han proporcionado todos los datos necesarios
    if not user_name or not password or not email:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Encriptar la contraseña
    encrypted_password = encrypt_password(password)

    # Conexión a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname='christiandb',
            user='atom',
            password='Maps2019!',
            host='82.223.110.207',
            port='5432'
        )
        cursor = conn.cursor()

        # Inserción del nuevo usuario en la tabla 'users'
        cursor.execute(
            """
            INSERT INTO users (user_name, password, email, role, company)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_name, encrypted_password, email, role, company)
        )

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")

# Crear la ventana principal
root = customtkinter.CTk()
root.title("Crear Nuevo Usuario")

# Crear los elementos de la interfaz de usuario
customtkinter.CTkLabel(root, text="Nombre de Usuario:").grid(row=0, column=0, sticky="w")
username_entry = customtkinter.CTkEntry(root)
username_entry.grid(row=0, column=1)

customtkinter.CTkLabel(root, text="Contraseña:").grid(row=1, column=0, sticky="w")
password_entry = customtkinter.CTkEntry(root, show="*")
password_entry.grid(row=1, column=1)

customtkinter.CTkLabel(root, text="Correo Electrónico:").grid(row=2, column=0, sticky="w")
email_entry = customtkinter.CTkEntry(root)
email_entry.grid(row=2, column=1)

customtkinter.CTkLabel(root, text="Rol:").grid(row=3, column=0, sticky="w")
role_var = customtkinter.StringVar(value="admin")
role_dropdown = customtkinter.CTkOptionMenu(root, values=["admin", "customer"],
                                            command=role_var,
                                            variable=role_var)
role_dropdown.grid(row=3, column=1)

customtkinter.CTkLabel(root, text="Introduzca la empresa:").grid(row=4, column=0, sticky="w")
company_entry = customtkinter.CTkEntry(root)
company_entry.grid(row=4, column=1)

create_button = customtkinter.CTkButton(root, text="Crear Usuario", command=create_user)
create_button.grid(row=5, column=0, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
