
from Base_de_datos import BaseDeDatos
from Encriptacion import Encriptador

class ManejoUsuarios:
    def __init__(self):
        self.encriptador = Encriptador()
        self.base_datos = BaseDeDatos()

    def registrar_usuario (self, username, nombre, contra, foto):

        nombre_encriptado = self.encriptador.encriptar(nombre)
        password_hash  = self.encriptador.hashear_contra(contra)

        with self.base_datos.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO usuarios (username, nombre, password_hash , foto)
            VALUES (?, ?, ?, ?)
            """, (username, nombre_encriptado, password_hash , foto))

        print("Usuario registrado")


    def login(self, username, contra):
        resultado = self.base_datos.buscar_usuario_por_username(username)

        if resultado is None:
            return False, "Usuario no existe"

        password_hash , nombre_enc, foto = resultado

        if not self.encriptador.verificar_contra(contra, password_hash ):
            print("contra incorrecta")
            return False

        nombre = self.encriptador.desencriptar(nombre_enc)

        print("usuario logueado")
        return True, nombre, foto

manejo_usuarios = ManejoUsuarios()

# username = input("Username:")
# nombre = input("Nombre:")
# contra = input("Contrasenna:")
# foto = input("Ruta_foto:")

# manejo_usuarios.registrar_usuario(username, nombre, contra, foto)



username_login = input("Introduzca su username:")
contra_login = input("Introduzca su contra:")

manejo_usuarios.login(username_login, contra_login)

