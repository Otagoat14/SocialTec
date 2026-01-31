import socket
import threading
from Registro import ManejoUsuarios
from Base_de_datos import BaseDeDatos
from Grafo import Grafo
from Encriptacion import Encriptador
import json

IP = "127.0.0.1"
PUERTO = 5001  

# Instancias globales
grafo_amistades = Grafo()
db = BaseDeDatos()
encriptador = Encriptador()

def inicializar_grafo():
    try:
        amistades = db.obtener_todas_las_amistades()
        grafo_amistades.construir_desde_bd(amistades)
        print(f"[INIT] Grafo inicializado con {len(amistades)} amistades")
    except Exception as e:
        print(f"[ERROR] Error al inicializar grafo: {e}")

def manejar_cliente(cliente, addr):
    print(f"[CONEXION] Cliente conectado desde {addr}")
    
    try:
        # Recibir datos del cliente
        buffer = ""
        while True:
            data = cliente.recv(1024).decode()
            if not data:
                break
            buffer += data
            if buffer.count("\n") >= 3:
                break
        
        mensajes = buffer.strip().split("\n")
        print(f"[DEBUG] Mensajes recibidos: {len(mensajes)} mensajes")
        
        if len(mensajes) < 3:
            print(f"[ERROR] Datos incompletos: solo {len(mensajes)} mensajes")
            cliente.sendall("ERROR|Datos incompletos".encode())
            return
        
        operacion = mensajes[2]
        print(f"[OPERACION] {operacion}")
        
        # ============ LOGIN ============
        if operacion == "login":
            username = mensajes[0]
            password = mensajes[1]
            
            print(f"[LOGIN] Usuario: {username}")
            
            manejo_usuarios = ManejoUsuarios()
            exito, user_id, nombre, foto = manejo_usuarios.login(username, password)
            
            if exito:
                respuesta = f"LOGIN_OK|{user_id}|{nombre}|{foto if foto else ''}"
                print(f"[SUCCESS] Login exitoso para {username}")
            else:
                respuesta = "LOGIN_FAIL|Usuario o contraseña incorrectos"
                print(f"[FAIL] Login fallido para {username}")
            
            cliente.sendall(respuesta.encode())
        
        # ============ REGISTRO ============
        elif operacion == "registro":
            try:
                username = mensajes[0]
                nombre = mensajes[1]
                password = mensajes[3]
                foto = mensajes[4] if len(mensajes) > 4 and mensajes[4] else None
                
                print(f"[REGISTRO] Intentando registrar:")
                print(f"  - Usuario: {username}")
                print(f"  - Nombre: {nombre}")
                print(f"  - Foto: {foto if foto else 'Sin foto'}")
                
                manejo_usuarios = ManejoUsuarios()
                exito = manejo_usuarios.registrar_usuario(username, nombre, password, foto)
                
                if exito:
                    grafo_amistades.crear_nodo(username)
                    respuesta = "REGISTRO_OK|Usuario registrado correctamente"
                    print(f"[SUCCESS] Usuario {username} registrado exitosamente")
                else:
                    respuesta = "REGISTRO_FAIL|Error al registrar usuario (puede ya existir)"
                    print(f"[FAIL] Fallo al registrar usuario {username}")
                
                cliente.sendall(respuesta.encode())
                
            except Exception as e:
                print(f"[EXCEPTION] Error en registro: {e}")
                import traceback
                traceback.print_exc()
                respuesta = f"REGISTRO_FAIL|Error interno: {str(e)}"
                try:
                    cliente.sendall(respuesta.encode())
                except:
                    print("[ERROR] No se pudo enviar respuesta de error")
        
        # ============ OBTENER AMIGOS ============
        elif operacion == "obtener_amigos":
            username = mensajes[0]
            user_id = db.obtener_id_usuario(username)
            
            if user_id:
                amigos = db.obtener_amigos(user_id)
                lista_amigos = []
                for amigo in amigos:
                    try:
                        nombre_desc = encriptador.desencriptar(amigo[2])
                    except:
                        nombre_desc = "Usuario"
                    
                    lista_amigos.append({
                        'id': amigo[0],
                        'username': amigo[1],
                        'nombre': nombre_desc,
                        'foto': amigo[3] if amigo[3] else '',
                        'fecha': str(amigo[4])
                    })
                
                respuesta = f"AMIGOS_OK|{json.dumps(lista_amigos)}"
            else:
                respuesta = "AMIGOS_FAIL|Usuario no encontrado"
            
            cliente.sendall(respuesta.encode())
        
        # ============ BUSCAR USUARIOS ============
        elif operacion == "buscar_usuarios":
            termino = mensajes[0]
            username_actual = mensajes[1]
            user_id = db.obtener_id_usuario(username_actual)
            
            if user_id:
                resultados = db.buscar_usuarios(termino, user_id)
                
                lista_resultados = []
                for resultado in resultados:
                    es_amigo = db.son_amigos(user_id, resultado[0])
                    solicitudes = db.obtener_solicitudes_pendientes(user_id)
                    tiene_solicitud = any(s[1] == resultado[0] for s in solicitudes)
                    
                    lista_resultados.append({
                        'id': resultado[0],
                        'username': resultado[1],
                        'foto': resultado[2] if resultado[2] else '',
                        'es_amigo': es_amigo,
                        'tiene_solicitud': tiene_solicitud
                    })
                
                respuesta = f"BUSCAR_OK|{json.dumps(lista_resultados)}"
            else:
                respuesta = "BUSCAR_FAIL|Error en la búsqueda"
            
            cliente.sendall(respuesta.encode())
        
        # ============ ENVIAR SOLICITUD DE AMISTAD ============
        elif operacion == "enviar_solicitud":
            username_remitente = mensajes[0]
            username_destinatario = mensajes[1]
            
            remitente_id = db.obtener_id_usuario(username_remitente)
            destinatario_id = db.obtener_id_usuario(username_destinatario)
            
            if remitente_id and destinatario_id:
                exito = db.enviar_solicitud_amistad(remitente_id, destinatario_id)
                if exito:
                    respuesta = "SOLICITUD_OK|Solicitud enviada correctamente"
                else:
                    respuesta = "SOLICITUD_FAIL|No se pudo enviar la solicitud"
            else:
                respuesta = "SOLICITUD_FAIL|Usuario no encontrado"
            
            cliente.sendall(respuesta.encode())
        
        # ============ OBTENER SOLICITUDES PENDIENTES ============
        elif operacion == "obtener_solicitudes":
            username = mensajes[0]
            user_id = db.obtener_id_usuario(username)
            
            if user_id:
                solicitudes = db.obtener_solicitudes_pendientes(user_id)
                
                lista_solicitudes = []
                for solicitud in solicitudes:
                    lista_solicitudes.append({
                        'id': solicitud[0],
                        'remitente_id': solicitud[1],
                        'username': solicitud[2],
                        'fecha': str(solicitud[3])
                    })
                
                respuesta = f"SOLICITUDES_OK|{json.dumps(lista_solicitudes)}"
            else:
                respuesta = "SOLICITUDES_FAIL|Usuario no encontrado"
            
            cliente.sendall(respuesta.encode())
        
        # ============ ACEPTAR SOLICITUD ============
        elif operacion == "aceptar_solicitud":
            solicitud_id = int(mensajes[0])
            username_aceptante = mensajes[1]
            
            with db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u1.username, u2.username
                    FROM solicitud_amistad s
                    JOIN usuarios u1 ON s.remitente_id = u1.id
                    JOIN usuarios u2 ON s.destinatario_id = u2.id
                    WHERE s.id = ?
                """, (solicitud_id,))
                resultado = cursor.fetchone()
            
            if resultado:
                username_remitente = resultado[0]
                username_destinatario = resultado[1]
                
                exito = db.aceptar_solicitud_amistad(solicitud_id)
                
                if exito:
                    if username_remitente not in grafo_amistades.grafo:
                        grafo_amistades.crear_nodo(username_remitente)
                    if username_destinatario not in grafo_amistades.grafo:
                        grafo_amistades.crear_nodo(username_destinatario)
                    
                    grafo_amistades.apuntar(username_remitente, username_destinatario)
                    respuesta = "ACEPTAR_OK|Solicitud aceptada"
                else:
                    respuesta = "ACEPTAR_FAIL|Error al aceptar solicitud"
            else:
                respuesta = "ACEPTAR_FAIL|Solicitud no encontrada"
            
            cliente.sendall(respuesta.encode())
        
        # ============ RECHAZAR SOLICITUD ============
        elif operacion == "rechazar_solicitud":
            solicitud_id = int(mensajes[0])
            
            exito = db.rechazar_solicitud_amistad(solicitud_id)
            
            if exito:
                respuesta = "RECHAZAR_OK|Solicitud rechazada"
            else:
                respuesta = "RECHAZAR_FAIL|Error al rechazar solicitud"
            
            cliente.sendall(respuesta.encode())
        
        # ============ ELIMINAR AMISTAD ============
        elif operacion == "eliminar_amistad":
            username1 = mensajes[0]
            username2 = mensajes[1]
            
            user_id1 = db.obtener_id_usuario(username1)
            user_id2 = db.obtener_id_usuario(username2)
            
            if user_id1 and user_id2:
                exito = db.eliminar_amistad(user_id1, user_id2)
                
                if exito:
                    grafo_amistades.eliminar_amistad(username1, username2)
                    respuesta = "ELIMINAR_OK|Amistad eliminada"
                else:
                    respuesta = "ELIMINAR_FAIL|Error al eliminar amistad"
            else:
                respuesta = "ELIMINAR_FAIL|Usuario no encontrado"
            
            cliente.sendall(respuesta.encode())
        
        # ============ OBTENER PERFIL USUARIO ============
        elif operacion == "obtener_perfil":
            username = mensajes[0]
            user_id = db.obtener_id_usuario(username)
            
            if user_id:
                usuario = db.obtener_usuario_por_id(user_id)
                if usuario:
                    try:
                        nombre_desc = encriptador.desencriptar(usuario[2])
                    except:
                        nombre_desc = "Usuario"
                    
                    perfil = {
                        'id': usuario[0],
                        'username': usuario[1],
                        'nombre': nombre_desc,
                        'foto': usuario[3] if usuario[3] else ''
                    }
                    respuesta = f"PERFIL_OK|{json.dumps(perfil)}"
                else:
                    respuesta = "PERFIL_FAIL|Usuario no encontrado"
            else:
                respuesta = "PERFIL_FAIL|Usuario no encontrado"
            
            cliente.sendall(respuesta.encode())
        
        # ============ OBTENER GRAFO (para InterfazServer) ============
        elif operacion == "obtener_grafo":
            grafo_dict = {k: list(v) for k, v in grafo_amistades.grafo.items()}
            respuesta = f"GRAFO_OK|{json.dumps(grafo_dict)}"
            cliente.sendall(respuesta.encode())
        
        else:
            respuesta = "ERROR|Operación no reconocida"
            print(f"[ERROR] Operación desconocida: {operacion}")
            cliente.sendall(respuesta.encode())
    
    except Exception as e:
        print(f"[EXCEPTION] Error manejando cliente: {e}")
        import traceback
        traceback.print_exc()
        try:
            cliente.sendall(f"ERROR|{str(e)}".encode())
        except:
            print("[ERROR] No se pudo enviar respuesta de error")
    
    finally:
        cliente.close()
        print(f"[DESCONEXION] Cliente {addr} desconectado")


# Inicializar el servidor
if __name__ == "__main__":
    print("="*60)
    print("        SERVIDOR SOCIALTEC - INICIANDO")
    print("="*60)
    
    inicializar_grafo()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PUERTO))
    server.listen()
    print(f"\n[OK] Servidor iniciado en {IP}:{PUERTO}")
    print(f"[OK] Esperando conexiones...\n")
    
    while True:
        try:
            cliente, addr = server.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(cliente, addr))
            hilo.start()
        except KeyboardInterrupt:
            print("\n[STOP] Servidor detenido por usuario")
            break
        except Exception as e:
            print(f"[ERROR] Error en el servidor: {e}")
    
    server.close()
    print("[EXIT] Servidor cerrado")
