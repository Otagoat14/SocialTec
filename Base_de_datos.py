import sqlite3

class BaseDeDatos :
    def __init__(self, nombre_archivo = "usuarios.db"):
        self.nombre_archivo = nombre_archivo
        self.crear_tabla()
        
    def conectar(self):
        return sqlite3.connect(self.nombre_archivo)
    
    def crear_tabla(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nombre BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                foto TEXT )
            """)

    def buscar_usuario_por_username(self, username):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT password_hash, nombre, foto
            FROM usuarios
            WHERE username = ?
            """, (username,))
            return cursor.fetchone()

    


            

