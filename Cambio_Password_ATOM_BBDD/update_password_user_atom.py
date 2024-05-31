import tkinter as tk
from tkinter import messagebox
import bcrypt
import psycopg2
import customtkinter

customtkinter.set_appearance_mode("#ffffff")
customtkinter.set_default_color_theme("blue")

# Función para encriptar la contraseña
def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Función para actualizar la contraseña del usuario
def update_password():
    # Obtener los datos del usuario y la nueva contraseña
    email = email_entry.get()
    new_password = password_entry.get()

    # Verificar que se han proporcionado todos los datos necesarios
    if not email or not new_password:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return

    # Encriptar la nueva contraseña
    encrypted_password = encrypt_password(new_password)

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

        # Actualizar la contraseña del usuario en la tabla 'users'
        cursor.execute(
            """
            UPDATE users
            SET password = %s
            WHERE email = %s
            """,
            (encrypted_password, email)
        )

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Éxito", "Contraseña actualizada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {str(e)}")

# Crear la ventana principal
root = customtkinter.CTk()
root.title("Actualizar Contraseña")

# Crear los elementos de la interfaz de usuario
customtkinter.CTkLabel(root, text="Correo electronico:").grid(row=0, column=0, sticky="w")
email_entry = customtkinter.CTkEntry(root)
email_entry.grid(row=0, column=1)

customtkinter.CTkLabel(root, text="Nueva Contraseña:").grid(row=1, column=0, sticky="w")
password_entry = customtkinter.CTkEntry(root, show="*")
password_entry.grid(row=1, column=1)

update_button = customtkinter.CTkButton(root, text="Actualizar Contraseña", command=update_password)
update_button.grid(row=2, column=0, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
