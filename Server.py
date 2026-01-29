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

    print(f"Tipo de operación: {mensajes[2]}")
    
    if mensajes[2] == "login":
        cliente_login = ManejoUsuarios()
        resultado = cliente_login.login(mensajes[0], mensajes[1])

        if resultado[0] == True:
            respuesta = "Login Exitoso"
            
        else:
            respuesta = "Login Fallido"
        

        cliente.sendall(respuesta.encode())

        
    elif mensajes[2] == "registro":
        cliente_registro = ManejoUsuarios()
        
        exito = cliente_registro.registrar_usuario(mensajes[0], mensajes[1], mensajes[3], mensajes[4])
        
        if exito:
            respuesta = "Registro Exitoso"
        else:
            respuesta = "Registro Fallido"
        
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