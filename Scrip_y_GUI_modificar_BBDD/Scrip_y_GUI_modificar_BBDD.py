import psycopg2
import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configuración inicial de customtkinter
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Tema de color: "blue", "green", "dark-blue"

# Función para conectarse a la base de datos
def connect_to_db():
    try:
        # Obtener las credenciales desde las variables de entorno
        dbname = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')

        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para obtener todas las tablas de la base de datos
def get_table_names():
    conn = connect_to_db()
    if not conn:
        return []

    try:
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            tables = cursor.fetchall()
        return [table[0] for table in tables]
    except Exception as e:
        print("Error al obtener nombres de tablas:", e)
        return []
    finally:
        conn.close()
        
def format_value(value, column_type):
    """
    Formatea el valor según el tipo de columna:
    - NULL si es 'None'.
    - Números se mantienen sin comillas.
    - Textos se colocan entre comillas.
    """
    if value == "None":
        return "NULL"

    if column_type in ("integer", "double precision", "numeric"):
        try:
            # Convertir a número si el tipo lo requiere
            float_value = float(value)
            return str(int(float_value)) if float_value.is_integer() else str(float_value)
        except ValueError:
            raise ValueError(f"El valor '{value}' no es válido para el tipo {column_type}.")

    if column_type in ("text", "character varying"):
        return f"'{value.replace('\'', '\'\'')}'"  # Escapar comillas simples en texto

    # Otros tipos, tratar como texto por defecto
    return f"'{value}'"
       
def get_column_types(table_name):
    """
    Obtiene los nombres y tipos de las columnas de una tabla.
    """
    conn = connect_to_db()
    if not conn:
        return {}

    try:
        query = f"""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            columns = cursor.fetchall()
        # Convertir a un diccionario {columna: tipo}
        return {col[0]: col[1] for col in columns}
    except Exception as e:
        print("Error al obtener tipos de columnas:", e)
        return {}
    finally:
        conn.close()

# Función para obtener datos de una tabla
def fetch_table_data(table_name):
    conn = connect_to_db()
    if not conn:
        return pd.DataFrame()  # Devuelve un DataFrame vacío si falla la conexión

    try:
        query = f'SELECT * FROM "{table_name}"'
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Error al obtener datos:", e)
        return pd.DataFrame()  # Devuelve un DataFrame vacío si hay error
    finally:
        conn.close()

# Función para actualizar la vista de tabla
def update_table_view(tree, data):
    tree.delete(*tree.get_children())
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

# Función para refrescar los datos de la tabla
def refresh_table(tree, table_name):
    new_data = fetch_table_data(table_name)
    update_table_view(tree, new_data)

# Mostrar los datos de la tabla en una GUI
def show_table(table_name):
    data = fetch_table_data(table_name)
    if data.empty:
        print("No hay datos para mostrar.")
        return

    # Crear ventana para mostrar la tabla
    table_window = ctk.CTkToplevel()
    table_window.title(f"Tabla: {table_name}")
    table_window.geometry("800x600")

    # Crear un marco para el Treeview y las barras de desplazamiento
    tree_frame = ctk.CTkFrame(table_window)
    tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Crear las barras de desplazamiento
    x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
    y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")

    # Crear el Treeview con las barras de desplazamiento
    tree = ttk.Treeview(
        tree_frame,
        columns=list(data.columns),
        show="headings",
        xscrollcommand=x_scrollbar.set,
        yscrollcommand=y_scrollbar.set,
    )

    # Configurar las barras de desplazamiento para el Treeview
    x_scrollbar.config(command=tree.xview)
    y_scrollbar.config(command=tree.yview)

    # Posicionar el Treeview y las barras de desplazamiento
    tree.grid(row=0, column=0, sticky="nsew")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")

    # Expandir el Treeview con el marco
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Configurar encabezados y columnas del Treeview
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Insertar los datos en el Treeview
    update_table_view(tree, data)

    # Crear el marco para los botones
    button_frame = ctk.CTkFrame(table_window)
    button_frame.pack(fill="x", pady=10)

    # Agregar los botones de acción
    ctk.CTkButton(button_frame, text="Añadir Registro", command=lambda: add_record_gui(table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Eliminar Registro", command=lambda: delete_record_gui(tree, table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Editar Registro", command=lambda: edit_record_gui(tree, table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Refrescar", command=lambda: refresh_table(tree, table_name)).pack(side="right", padx=5)

# Interfaz principal para seleccionar tabla
import customtkinter as ctk

# Interfaz principal para seleccionar tabla
def main_gui():
    root = ctk.CTk()
    root.title("Explorador de Base de Datos")
    root.geometry("400x300")

    # Obtener los nombres de las tablas
    tables = get_table_names()
    if not tables:
        ctk.CTkLabel(root, text="No se encontraron tablas. Verifica la conexión a la base de datos.").pack(pady=10)
        root.mainloop()
        return

    # Etiqueta de instrucción
    ctk.CTkLabel(root, text="Selecciona una tabla:").pack(pady=10)

    # Combobox personalizado
    table_combobox = ctk.CTkComboBox(
        root,
        values=tables,
        width=250,  # Ajustar el ancho del combobox
        height=30,  # Ajustar la altura del combobox
        state="readonly"
    )
    table_combobox.pack(pady=10)
    table_combobox.set("Selecciona una tabla")  # Texto inicial

    # Botón para abrir la tabla seleccionada
    ctk.CTkButton(root, text="Abrir Tabla", command=lambda: show_table(table_combobox.get())).pack(pady=10)

    root.mainloop()

# Función para añadir un registro
def add_record_gui(table_name):
    def save_record():
        record = {entry[0]: entry[1].get() for entry in entries}
        add_record(table_name, record)
        add_window.destroy()

    add_window = ctk.CTkToplevel()
    add_window.title(f"Añadir Registro en {table_name}")
    add_window.geometry("400x400")

    columns = fetch_table_data(table_name).columns
    entries = []

    # Usar un contenedor scrollable para los campos de entrada
    scrollable_frame = ctk.CTkScrollableFrame(add_window, width=350, height=300)
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    for col in columns:
        ctk.CTkLabel(scrollable_frame, text=col).pack(pady=5)
        entry = ctk.CTkEntry(scrollable_frame)
        entry.pack(pady=5, fill="x")
        entries.append((col, entry))

    ctk.CTkButton(add_window, text="Guardar", command=save_record).pack(pady=10)

# Función para actualizar la vista de la tabla con filtro de búsqueda
def search_table(tree, data, search_value):
    filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]
    update_table_view(tree, filtered_data)
    if filtered_data.empty:
        no_results_label = ctk.CTkLabel(tree_frame, text="No se encontraron registros.", text_color="red")
        no_results_label.grid(row=1, column=0, pady=10)

# Función para mostrar la tabla con el buscador
def show_table(table_name):
    data = fetch_table_data(table_name)
    if data.empty:
        print("No hay datos para mostrar.")
        return

    # Crear ventana para mostrar la tabla
    table_window = ctk.CTkToplevel()
    table_window.title(f"Tabla: {table_name}")
    table_window.geometry("800x600")

    # Crear un marco para el Treeview y las barras de desplazamiento
    tree_frame = ctk.CTkFrame(table_window)
    tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Crear las barras de desplazamiento
    x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
    y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")

    # Crear el Treeview con las barras de desplazamiento
    tree = ttk.Treeview(
        tree_frame,
        columns=list(data.columns),
        show="headings",
        xscrollcommand=x_scrollbar.set,
        yscrollcommand=y_scrollbar.set,
    )

    # Configurar las barras de desplazamiento para el Treeview
    x_scrollbar.config(command=tree.xview)
    y_scrollbar.config(command=tree.yview)

    # Posicionar el Treeview y las barras de desplazamiento
    tree.grid(row=0, column=0, sticky="nsew")
    x_scrollbar.grid(row=1, column=0, sticky="ew")
    y_scrollbar.grid(row=0, column=1, sticky="ns")

    # Expandir el Treeview con el marco
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Configurar encabezados y columnas del Treeview
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    # Insertar los datos en el Treeview
    update_table_view(tree, data)

    # Añadir campo de búsqueda
    search_frame = ctk.CTkFrame(table_window)
    search_frame.pack(fill="x", pady=10)
    
    ctk.CTkLabel(search_frame, text="Buscar:").pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200)
    search_entry.pack(side="left", padx=5)
    
    # Función para actualizar el Treeview con el valor de búsqueda
    def on_search():
        search_value = search_entry.get()
        search_table(tree, data, search_value)
    
    # Botón de búsqueda
    search_button = ctk.CTkButton(search_frame, text="Buscar", command=on_search)
    search_button.pack(side="left", padx=5)

    # Crear el marco para los botones
    button_frame = ctk.CTkFrame(table_window)
    button_frame.pack(fill="x", pady=10)

    # Agregar los botones de acción
    ctk.CTkButton(button_frame, text="Añadir Registro", command=lambda: add_record_gui(table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Eliminar Registro", command=lambda: delete_record_gui(tree, table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Editar Registro", command=lambda: edit_record_gui(tree, table_name)).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Refrescar", command=lambda: refresh_table(tree, table_name)).pack(side="right", padx=5)


# Lógica para añadir un registro a la base de datos
def add_record(table_name, record):
    conn = connect_to_db()
    if not conn:
        return

    try:
        columns = ", ".join(record.keys())
        values = ", ".join(f"'{v}'" for v in record.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
        print("Registro añadido correctamente.")
    except Exception as e:
        print("Error al añadir registro:", e)
    finally:
        conn.close()

# Función para eliminar un registro
def delete_record_gui(tree, table_name):
    selected_item = tree.selection()
    if not selected_item:
        print("Selecciona un registro para eliminar.")
        return

    values = tree.item(selected_item, "values")
    delete_record(table_name, values[0])
    tree.delete(selected_item)

def delete_record(table_name, primary_key_value):
    conn = connect_to_db()
    if not conn:
        return

    try:
        query = f"DELETE FROM {table_name} WHERE id = {primary_key_value}"  # Cambiar 'id' según sea necesario
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
        print("Registro eliminado correctamente.")
    except Exception as e:
        print("Error al eliminar registro:", e)
    finally:
        conn.close()

# Función para abrir la ventana de edición
def edit_record_gui(tree, table_name):
    selected_item = tree.selection()
    if not selected_item:
        print("Selecciona un registro para editar.")
        return

    values = tree.item(selected_item, "values")
    if not values:
        print("No se encontraron valores en el registro seleccionado.")
        return

    # Crear una ventana para editar el registro
    edit_window = ctk.CTkToplevel()
    edit_window.title(f"Editar Registro en {table_name}")
    edit_window.geometry("600x600")  # Tamaño más grande
    edit_window.resizable(True, True)  # Permitir redimensionar

    # Crear campos de entrada dinámicos
    columns = fetch_table_data(table_name).columns
    entries = []

    # Usar un contenedor scrollable para manejar muchas columnas
    scrollable_frame = ctk.CTkScrollableFrame(edit_window, width=550, height=500)
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    for i, col in enumerate(columns):
        ctk.CTkLabel(scrollable_frame, text=col).pack(pady=5)
        entry = ctk.CTkEntry(scrollable_frame)
        entry.insert(0, values[i])  # Prellenar con el valor actual
        entry.pack(pady=5, fill="x")
        entries.append((col, entry))

    # Botón para guardar los cambios
    ctk.CTkButton(
        edit_window,
        text="Guardar Cambios",
        command=lambda: save_edited_record(table_name, values[0], entries, edit_window)
    ).pack(pady=10)

# Función para guardar los cambios en la base de datos
def save_edited_record(table_name, primary_key_value, entries, edit_window):
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Obtener tipos de columnas
        column_types = get_column_types(table_name)

        # Construir la cláusula SET
        set_clause = ", ".join(
            f'"{col}" = {format_value(entry.get(), column_types[col])}' for col, entry in entries
        )
        # Usar la clave primaria para identificar el registro
        query = f'UPDATE "{table_name}" SET {set_clause} WHERE "ID_PLANTA" = \'{primary_key_value}\''

        print("Consulta generada:", query)  # Para depuración

        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

        print("Registro actualizado correctamente.")
        edit_window.destroy()
    except Exception as e:
        print("Error al actualizar registro:", e)
    finally:
        conn.close()

# Iniciar la aplicación
if __name__ == "__main__":
    main_gui()
