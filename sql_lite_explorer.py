import sqlite3
import os
import sys

def listar_tablas_y_conteo(db_path):
    """Lista todas las tablas y el número de registros en cada una."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"Analizando la base de datos: '{db_path}'\n")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        if not tablas:
            print("No se encontraron tablas en la base de datos.")
            return

        print("Recuento de registros por tabla:")
        for tabla_tupla in tablas:
            nombre_tabla = tabla_tupla[0]
            cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla};")
            num_registros = cursor.fetchone()[0]
            print(f"- '{nombre_tabla}': {num_registros} registros")

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def visualizar_registros(db_path, nombre_tabla):
    """Muestra todos los registros de una tabla específica."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (nombre_tabla,))
        if not cursor.fetchone():
            print(f"Error: La tabla '{nombre_tabla}' no existe en la base de datos.")
            return

        print(f"\nMostrando el contenido de la tabla '{nombre_tabla}'...\n")

        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas = [col[1] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {nombre_tabla};")
        filas = cursor.fetchall()

        if not filas:
            print(f"La tabla '{nombre_tabla}' está vacía.")
            return

        print("-" * 50)
        print(" | ".join(columnas))
        print("-" * 50)

        for fila in filas:
            print(" | ".join(map(str, fila)))

        print("-" * 50)

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("Para listar tablas: python sqlite_explorer.py <ruta_al_archivo.db>")
        print("Para ver registros: python sqlite_explorer.py <ruta_al_archivo.db> -registros <nombre_de_la_tabla>")
        sys.exit(1)
    
    ruta_db = sys.argv[1]

    if not os.path.exists(ruta_db):
        print(f"Error: No se encontró el archivo de base de datos '{ruta_db}'")
        sys.exit(1)

    if len(sys.argv) == 2:
        listar_tablas_y_conteo(ruta_db)
    elif len(sys.argv) == 4 and sys.argv[2] == '-registros':
        nombre_tabla = sys.argv[3]
        visualizar_registros(ruta_db, nombre_tabla)
    else:
        print("Uso incorrecto. Por favor, revisa las opciones.")
        print("Para listar tablas: python sqlite_explorer.py <ruta_al_archivo.db>")
        print("Para ver registros: python sqlite_explorer.py <ruta_al_archivo.db> -registros <nombre_de_la_tabla>")
