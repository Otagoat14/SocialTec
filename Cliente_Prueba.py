import socket
import json

class ClienteTCP:
    def __init__(self):
        self.cliente = None
    
    def conectar(self, ip, puerto):
        """Conectar al servidor"""
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((ip, puerto))
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
    
    def enviar(self, mensaje):
        """Enviar un mensaje al servidor"""
        try:
            self.cliente.sendall(f"{mensaje}\n".encode())
        except Exception as e:
            print(f"Error al enviar: {e}")
    
    def recibir(self, buffer_size=4096):
        """Recibir respuesta del servidor"""
        try:
            respuesta = self.cliente.recv(buffer_size).decode()
            return respuesta
        except Exception as e:
            print(f"Error al recibir: {e}")
            return None
    
    def recibir_json(self, buffer_size=4096):
        """Recibir respuesta JSON del servidor"""
        try:
            respuesta = self.cliente.recv(buffer_size).decode()
            return json.loads(respuesta)
        except json.JSONDecodeError:
            print("Error: La respuesta no es un JSON válido")
            return None
        except Exception as e:
            print(f"Error al recibir JSON: {e}")
            return None
    
    def cerrar(self):
        """Cerrar la conexión"""
        if self.cliente:
            self.cliente.close()