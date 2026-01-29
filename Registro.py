from Base_de_datos import BaseDeDatos
from Encriptacion import Encriptador

class ManejoUsuarios:
    def __init__(self):
        self.encriptador = Encriptador()
        self.base_datos = BaseDeDatos()

    def registrar_usuario(self, username, nombre, contra, foto=None):
        try:
            
            nombre_encriptado = self.encriptador.encriptar(nombre)
            password_hash = self.encriptador.hashear_contra(contra)

            with self.base_datos.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO usuarios (username, nombre, password_hash, foto)
                VALUES (?, ?, ?, ?)
                """, (username, nombre_encriptado, password_hash, foto))
                
                
                conn.commit()

            print("Usuario registrado correctamente")
            return True
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def login(self, username, contra):
  
        resultado = self.base_datos.buscar_usuario_por_username(username)

        if resultado is None:
            print("Usuario no existe")
            return False, None, None, None

        password_hash, nombre_enc, foto = resultado

        if not self.encriptador.verificar_contra(contra, password_hash):
            print("Contraseña incorrecta")
            return False, None, None, None


        nombre = self.encriptador.desencriptar(nombre_enc)
        
        user_id = self.base_datos.obtener_id_usuario(username)

        print(f"Bienvenido {nombre}!")
        return True, user_id, nombre, foto

