import os
import hashlib
from cryptography.fernet import Fernet

class Encriptador:
    def __init__(self, key_ruta = "secret.key"):
        with open (key_ruta, "rb") as f:
            self.fernet = Fernet(f.read())

    def encriptar (self, dato):
        return self.fernet.encrypt(dato.encode())

    
    def desencriptar(self, dato_encriptado):
        return self.fernet.decrypt(dato_encriptado).decode()

        
    def hashear_contra (self, contra_sin_hash):
        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", contra_sin_hash.encode(), salt, 100_000)
        contra_hasheada = salt + hash_bytes
        return contra_hasheada

    def verificar_contra (self, contra_sin_hash, contra_hasheada):
        salt = contra_hasheada[: 16]
        hash_guardado = contra_hasheada[16 : ]
        nuevo_hash = hashlib.pbkdf2_hmac("sha256", contra_sin_hash.encode(), salt, 100_000)

        return hash_guardado == nuevo_hash
    








