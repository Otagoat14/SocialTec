import sqlite3
<<<<<<< HEAD

class BaseDeDatos :
    def __init__(self, nombre_archivo = "usuarios.db"):
        self.nombre_archivo = nombre_archivo
        self.crear_tabla()
        
    def conectar(self):
        return sqlite3.connect(self.nombre_archivo)
    
    def crear_tabla(self):
=======
from datetime import datetime

class BaseDeDatos:
    def __init__(self, nombre_db="usuarios.db"):
        self.nombre_db = nombre_db
        
        self.crear_tabla_usuarios()
        self.crear_tabla_amistades()
        self.crear_tabla_solicitud_amistad()
    
    def conectar(self):
        return sqlite3.connect(self.nombre_db)
    
    # ========================================
    # MÉTODOS PARA CREAR TABLAS
    # ========================================
    
    def crear_tabla_usuarios(self):
        """Crear la tabla de usuarios (tu tabla original)"""
>>>>>>> d059e9bcf077a9a26bfd10513af49c421b2dcf0d
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nombre BLOB NOT NULL,
                password_hash BLOB NOT NULL,
<<<<<<< HEAD
                foto TEXT )
            """)

    def buscar_usuario_por_username(self, username):
=======
                foto TEXT
            )
            """)
            conn.commit()
    
    def crear_tabla_amistades(self):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS amistades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                amigo_id INTEGER NOT NULL,
                fecha_amistad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (amigo_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                UNIQUE(usuario_id, amigo_id),
                CHECK(usuario_id != amigo_id)
            )
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_amistades_usuario 
            ON amistades(usuario_id)
            """)
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_amistades_amigo 
            ON amistades(amigo_id)
            """)
            conn.commit()
    
    def crear_tabla_solicitud_amistad(self):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitud_amistad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente_id INTEGER NOT NULL,
                destinatario_id INTEGER NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (remitente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (destinatario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                UNIQUE(remitente_id, destinatario_id),
                CHECK(remitente_id != destinatario_id)
            )
            """)
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_solicitudes_destinatario 
            ON solicitud_amistad(destinatario_id)
            """)
            conn.commit()
    
    #BSUCAR USUARIOS E ID

    def buscar_usuario_por_username(self, username):

>>>>>>> d059e9bcf077a9a26bfd10513af49c421b2dcf0d
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT password_hash, nombre, foto
            FROM usuarios
            WHERE username = ?
            """, (username,))
            return cursor.fetchone()
<<<<<<< HEAD

    


            
=======
    
    def obtener_id_usuario(self, username):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id FROM usuarios WHERE username = ?
            """, (username,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    
    def obtener_usuario_por_id(self, usuario_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, username, nombre, foto
            FROM usuarios
            WHERE id = ?
            """, (usuario_id,))
            return cursor.fetchone()
    
    # SOLICUTDES DE AMISTAD
    
    def enviar_solicitud_amistad(self, remitente_id, destinatario_id):

        if remitente_id == destinatario_id:
            print("No puedes enviarte solicitud a ti mismo")
            return False
        
        with self.conectar() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            SELECT id FROM amistades 
            WHERE usuario_id = ? AND amigo_id = ?
            """, (remitente_id, destinatario_id))
            
            if cursor.fetchone():
                print("Ya son amigos")
                return False

            cursor.execute("""
            SELECT id FROM solicitud_amistad 
            WHERE ((remitente_id = ? AND destinatario_id = ?) 
                OR (remitente_id = ? AND destinatario_id = ?))
                AND estado = 'pendiente'
            """, (remitente_id, destinatario_id, destinatario_id, remitente_id))
            
            if cursor.fetchone():
                print("Ya existe una solicitud pendiente")
                return False
            
            try:
                cursor.execute("""
                INSERT INTO solicitud_amistad (remitente_id, destinatario_id)
                VALUES (?, ?)
                """, (remitente_id, destinatario_id))
                conn.commit()
                print("Solicitud enviada correctamente")
                return True
            
            except sqlite3.IntegrityError as e:
                print(f"Error al enviar solicitud: {e}")
                return False
    
    def obtener_solicitudes_pendientes(self, usuario_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT s.id, s.remitente_id, u.username, s.fecha_solicitud
            FROM solicitud_amistad s
            JOIN usuarios u ON s.remitente_id = u.id
            WHERE s.destinatario_id = ? AND s.estado = 'pendiente'
            ORDER BY s.fecha_solicitud DESC
            """, (usuario_id,))
            return cursor.fetchall()
    
    def aceptar_solicitud_amistad(self, solicitud_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
       
            cursor.execute("""
            SELECT remitente_id, destinatario_id 
            FROM solicitud_amistad 
            WHERE id = ? AND estado = 'pendiente'
            """, (solicitud_id,))
            
            resultado = cursor.fetchone()
            if not resultado:
                print("Solicitud no encontrada")
                return False
            
            remitente_id, destinatario_id = resultado
            
            try:
            
                cursor.execute("""
                INSERT INTO amistades (usuario_id, amigo_id)
                VALUES (?, ?), (?, ?)
                """, (remitente_id, destinatario_id, destinatario_id, remitente_id))

                cursor.execute("""
                UPDATE solicitud_amistad 
                SET estado = 'aceptada'
                WHERE id = ?
                """, (solicitud_id,))
                
                conn.commit()
                print("Solicitud aceptada")
                return True
                
            except sqlite3.IntegrityError as e:
                print(f"Error al aceptar solicitud: {e}")
                return False
    
    def rechazar_solicitud_amistad(self, solicitud_id):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE solicitud_amistad 
            SET estado = 'rechazada'
            WHERE id = ? AND estado = 'pendiente'
            """, (solicitud_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                print("Solicitud rechazada")
                return True
            else:
                print("Solicitud no encontrada o ya fue procesada")
                return False
    
    #GESTION DE LAS AMISTADES   
    
    def obtener_amigos(self, usuario_id):
    
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT u.id, u.username, u.nombre, u.foto, a.fecha_amistad
            FROM amistades a
            JOIN usuarios u ON a.amigo_id = u.id
            WHERE a.usuario_id = ?
            ORDER BY a.fecha_amistad DESC
            """, (usuario_id,))
            return cursor.fetchall()
    
    def eliminar_amistad(self, usuario_id, amigo_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            DELETE FROM amistades 
            WHERE (usuario_id = ? AND amigo_id = ?) 
               OR (usuario_id = ? AND amigo_id = ?)
            """, (usuario_id, amigo_id, amigo_id, usuario_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                print("Amistad eliminada")
                return True
            else:
                print("No se encontró la amistad")
                return False
    
    def son_amigos(self, usuario_id, amigo_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id FROM amistades 
            WHERE usuario_id = ? AND amigo_id = ?
            """, (usuario_id, amigo_id))
            return cursor.fetchone() is not None
    
    def contar_amigos(self, usuario_id):

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT COUNT(*) FROM amistades WHERE usuario_id = ?
            """, (usuario_id,))
            return cursor.fetchone()[0]
  

    # MÉTODOS DE BÚSQUEDA
    
    
    def buscar_usuarios(self, termino, excluir_usuario_id=None):
      
        with self.conectar() as conn:
            cursor = conn.cursor()
            
            if excluir_usuario_id:
                cursor.execute("""
                SELECT id, username, foto 
                FROM usuarios 
                WHERE username LIKE ? AND id != ?
                LIMIT 20
                """, (f'%{termino}%', excluir_usuario_id))
            else:
                cursor.execute("""
                SELECT id, username, foto 
                FROM usuarios 
                WHERE username LIKE ?
                LIMIT 20
                """, (f'%{termino}%',))
            
            return cursor.fetchall()
    
    def buscar_no_amigos(self, usuario_id, termino):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT u.id, u.username, u.foto 
            FROM usuarios u
            WHERE u.username LIKE ? 
              AND u.id != ?
              AND u.id NOT IN (
                  SELECT amigo_id FROM amistades WHERE usuario_id = ?
              )
            LIMIT 20
            """, (f'%{termino}%', usuario_id, usuario_id))
            return cursor.fetchall()
>>>>>>> d059e9bcf077a9a26bfd10513af49c421b2dcf0d

