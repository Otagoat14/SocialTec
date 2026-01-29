import socket

puerto = 5001
ip = "127.0.0.1"

class ClienteTCP:
    def __init__(self):
        self.cliente = None

    def conectar(self, ip, puerto):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((ip, puerto))
        print("Conectado al servidor")

    def enviar(self, mensaje):
        datos = (mensaje + "\n").encode("utf-8") 
        self.cliente.sendall(datos)
        print("Mensaje enviado:", mensaje)

    def recibir(self):
        buffer = self.cliente.recv(1024)
        return buffer.decode("utf-8")

    def cerrar(self):
        self.cliente.close()
        print("Conexión cerrada")
