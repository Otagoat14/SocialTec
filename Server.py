import socket
import threading
from Enrutador import enrutador

IP = "127.0.0.1"
PUERTO = 5000

def manejar_cliente(cliente, addr):
    print("Cliente recibido")

    mensaje = cliente.recv(1024).decode()
    print("Mensaje recibido")

    mensaje_temp = "login"
    respuesta = enrutador(mensaje_temp)

    cliente.sendall(respuesta.encode())

    cliente.close()
    print("Cliente atendido")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PUERTO))
server.listen()
print("Servidor iniciado")

while True:
    cliente, addr = server.accept()

    hilo = threading.Thread(target=manejar_cliente, args=(cliente, addr))
    hilo.start()
