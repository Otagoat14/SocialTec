import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print("Conectado al servidor")

    cliente.sendall("Hola servidor\n".encode("utf-8"))
    print("Mensaje 1 enviado")

    cliente.sendall("Este es el segundo mensaje\n".encode("utf-8"))
    print("Mensaje 2 enviado")

    respuesta = cliente.recv(1024).decode()
    print("Respuesta del servidor:", respuesta)

print("Conexión cerrada")
