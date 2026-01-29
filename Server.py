import socket
import threading
from Registro import ManejoUsuarios

IP = "127.0.0.1"
PUERTO = 5000

def manejar_cliente(cliente, addr):
    print("Cliente recibido")

    buffer = ""

    while buffer.count("\n") < 2:
        data = cliente.recv(1024).decode()
        if not data:
            break
        buffer += data

    mensajes = buffer.strip().split("\n")

    mensaje1 = mensajes[0]
    mensaje2 = mensajes[1]
    mensaje3 = mensajes[2]
    
    if mensaje3 == "login":
        cliente_login = ManejoUsuarios()
        respuesta = cliente_login.login(mensaje1, mensaje2)
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
