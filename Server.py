import socket
import threading
import json
from Registro import ManejoUsuarios
from Grafo import *
from Base_de_datos import *

IP = "127.0.0.1"
PUERTO = 5000

def manejar_cliente(cliente, addr):
    print(f"✓ Cliente conectado desde {addr}")

    buffer = ""
    db = BaseDeDatos()

    try:
        # Recibir datos del cliente
        while True:
            data = cliente.recv(1024).decode()
            if not data:
                break
            buffer += data
            
            # Contar líneas recibidas
            lineas = buffer.count("\n")
            
            # Para login y registro necesitamos al menos 3 líneas
            # Para buscar necesitamos al menos 3 líneas también
            if lineas >= 3:
                break

        print(f"📨 Buffer recibido: {repr(buffer[:100])}")  # Solo primeros 100 chars
        
        # Separar los mensajes y limpiar espacios
        mensajes = [m.strip() for m in buffer.strip().split("\n") if m.strip()]
        
        if not mensajes:
            print("❌ No se recibieron mensajes")
            cliente.sendall("Error: No hay mensajes".encode())
            return
            
        comando = mensajes[0]
        print(f"🔧 Comando: {comando}")
        print(f"📝 Total parámetros: {len(mensajes)-1}")
        
        # ========== LOGIN ==========
        if comando == "login":
            if len(mensajes) < 3:
                print("❌ Login: Faltan parámetros")
                cliente.sendall("Login Fallido".encode())
                return
                
            username = mensajes[1]
            password = mensajes[2]
            
            print(f"🔐 Login: usuario='{username}'")
            
            cliente_login = ManejoUsuarios()
            resultado = cliente_login.login(username, password)

            if resultado[0] == True:
                respuesta = "Login Exitoso"
                print(f"✅ Login exitoso para {username}")
            else:
                respuesta = "Login Fallido"
                print(f"❌ Login fallido para {username}")
            
            cliente.sendall(respuesta.encode())

        # ========== REGISTRO ==========
        elif comando == "registro":
            if len(mensajes) < 5:
                print("❌ Registro: Faltan parámetros")
                cliente.sendall("Registro Fallido".encode())
                return
                
            username = mensajes[1]
            nombre = mensajes[2]
            password = mensajes[3]
            foto = mensajes[4]
            
            print(f"📝 Registro: usuario='{username}', nombre='{nombre}'")
            
            cliente_registro = ManejoUsuarios()
            exito = cliente_registro.registrar_usuario(username, nombre, password, foto)
            
            if exito:
                respuesta = "Registro Exitoso"
                print(f"✅ Usuario {username} registrado correctamente")
            else:
                respuesta = "Registro Fallido"
                print(f"❌ Error al registrar {username}")
            
            cliente.sendall(respuesta.encode())

        # ========== BUSCAR USUARIOS ==========
        elif comando == "buscar":
            if len(mensajes) < 3:
                print("❌ Buscar: Faltan parámetros")
                cliente.sendall("[]".encode())
                return
                
            termino_busqueda = mensajes[1]
            usuario_actual = mensajes[2]
            
            print(f"🔍 Búsqueda: término='{termino_busqueda}', usuario='{usuario_actual}'")
            
            # Obtener el ID del usuario actual
            usuario_id = db.obtener_id_usuario(usuario_actual)
            
            if not usuario_id:
                print(f"❌ Usuario '{usuario_actual}' no encontrado")
                cliente.sendall("[]".encode())
                return
            
            print(f"✓ ID usuario: {usuario_id}")
            
            # Buscar usuarios que coincidan con el término
            resultados = db.buscar_usuarios(termino_busqueda, usuario_id)
            print(f"📊 Encontrados: {len(resultados)} resultados")
            
            # Para cada resultado, verificar si ya son amigos
            resultados_completos = []
            for resultado in resultados:
                resultado_id, username, foto = resultado
                es_amigo = db.son_amigos(usuario_id, resultado_id)
                
                resultados_completos.append({
                    'id': resultado_id,
                    'username': username,
                    'foto': foto if foto else "sin_foto",
                    'es_amigo': es_amigo
                })
                print(f"  - {username} (ID:{resultado_id}, amigo:{es_amigo})")
            
            # Convertir a JSON y enviar
            respuesta = json.dumps(resultados_completos)
            print(f"📤 Enviando JSON: {len(respuesta)} bytes")
            cliente.sendall(respuesta.encode())

        # ========== ENVIAR SOLICITUD DE AMISTAD ==========
        elif comando == "solicitar_amistad":
            if len(mensajes) < 3:
                print("❌ Solicitar amistad: Faltan parámetros")
                cliente.sendall("Error al enviar solicitud".encode())
                return
                
            usuario_actual = mensajes[1]
            usuario_destino = mensajes[2]
            
            print(f"👥 Solicitud de amistad: {usuario_actual} → {usuario_destino}")
            
            # Obtener IDs
            remitente_id = db.obtener_id_usuario(usuario_actual)
            destinatario_id = db.obtener_id_usuario(usuario_destino)
            
            if remitente_id and destinatario_id:
                exito = db.enviar_solicitud_amistad(remitente_id, destinatario_id)
                respuesta = "Solicitud enviada" if exito else "Error al enviar solicitud"
                print(f"{'✅' if exito else '❌'} {respuesta}")
            else:
                respuesta = "Usuario no encontrado"
                print(f"❌ {respuesta}")
            
            cliente.sendall(respuesta.encode())

        # ========== ELIMINAR AMISTAD ==========
        elif comando == "eliminar_amistad":
            if len(mensajes) < 3:
                print("❌ Eliminar amistad: Faltan parámetros")
                cliente.sendall("Error al eliminar amistad".encode())
                return
                
            usuario_actual = mensajes[1]
            usuario_amigo = mensajes[2]
            
            print(f"💔 Eliminar amistad: {usuario_actual} ✗ {usuario_amigo}")
            
            # Obtener IDs
            usuario_id = db.obtener_id_usuario(usuario_actual)
            amigo_id = db.obtener_id_usuario(usuario_amigo)
            
            if usuario_id and amigo_id:
                exito = db.eliminar_amistad(usuario_id, amigo_id)
                respuesta = "Amistad eliminada" if exito else "Error al eliminar amistad"
                print(f"{'✅' if exito else '❌'} {respuesta}")
            else:
                respuesta = "Usuario no encontrado"
                print(f"❌ {respuesta}")
            
            cliente.sendall(respuesta.encode())

        # ========== OBTENER SOLICITUDES PENDIENTES ==========
        elif comando == "solicitudes_pendientes":
            if len(mensajes) < 2:
                print("❌ Solicitudes pendientes: Faltan parámetros")
                cliente.sendall("[]".encode())
                return
                
            usuario_actual = mensajes[1]
            usuario_id = db.obtener_id_usuario(usuario_actual)
            
            print(f"📬 Obteniendo solicitudes para: {usuario_actual}")
            
            if usuario_id:
                solicitudes = db.obtener_solicitudes_pendientes(usuario_id)
                solicitudes_json = []
                for solicitud in solicitudes:
                    solicitudes_json.append({
                        'id': solicitud[0],
                        'remitente_id': solicitud[1],
                        'username': solicitud[2],
                        'fecha': str(solicitud[3])
                    })
                respuesta = json.dumps(solicitudes_json)
                print(f"✓ {len(solicitudes)} solicitudes pendientes")
            else:
                respuesta = json.dumps([])
                print("❌ Usuario no encontrado")
            
            cliente.sendall(respuesta.encode())

        # ========== ACEPTAR SOLICITUD ==========
        elif comando == "aceptar_solicitud":
            if len(mensajes) < 2:
                print("❌ Aceptar solicitud: Faltan parámetros")
                cliente.sendall("Error al aceptar".encode())
                return
                
            solicitud_id = int(mensajes[1])
            print(f"✅ Aceptando solicitud ID: {solicitud_id}")
            
            exito = db.aceptar_solicitud_amistad(solicitud_id)
            respuesta = "Solicitud aceptada" if exito else "Error al aceptar"
            print(f"{'✅' if exito else '❌'} {respuesta}")
            cliente.sendall(respuesta.encode())

        # ========== RECHAZAR SOLICITUD ==========
        elif comando == "rechazar_solicitud":
            if len(mensajes) < 2:
                print("❌ Rechazar solicitud: Faltan parámetros")
                cliente.sendall("Error al rechazar".encode())
                return
                
            solicitud_id = int(mensajes[1])
            print(f"❌ Rechazando solicitud ID: {solicitud_id}")
            
            exito = db.rechazar_solicitud_amistad(solicitud_id)
            respuesta = "Solicitud rechazada" if exito else "Error al rechazar"
            print(f"{'✅' if exito else '❌'} {respuesta}")
            cliente.sendall(respuesta.encode())

        # ========== OBTENER AMIGOS ==========
        elif comando == "obtener_amigos":
            if len(mensajes) < 2:
                print("❌ Obtener amigos: Faltan parámetros")
                cliente.sendall("[]".encode())
                return
                
            usuario_actual = mensajes[1]
            usuario_id = db.obtener_id_usuario(usuario_actual)
            
            print(f"👥 Obteniendo amigos de: {usuario_actual}")
            
            if usuario_id:
                amigos = db.obtener_amigos(usuario_id)
                amigos_json = []
                for amigo in amigos:
                    try:
                        nombre_dec = amigo[2].decode() if isinstance(amigo[2], bytes) else amigo[2]
                    except:
                        nombre_dec = "Usuario"
                    
                    amigos_json.append({
                        'id': amigo[0],
                        'username': amigo[1],
                        'nombre': nombre_dec,
                        'foto': amigo[3] if amigo[3] else "sin_foto",
                        'fecha_amistad': str(amigo[4])
                    })
                respuesta = json.dumps(amigos_json)
                print(f"✓ {len(amigos)} amigos encontrados")
            else:
                respuesta = json.dumps([])
                print("❌ Usuario no encontrado")
            
            cliente.sendall(respuesta.encode())

        else:
            respuesta = f"Comando no reconocido: {comando}"
            print(f"❌ {respuesta}")
            cliente.sendall(respuesta.encode())

    except Exception as e:
        print(f"❌ Error al manejar cliente: {e}")
        import traceback
        traceback.print_exc()
        try:
            cliente.sendall(f"Error: {str(e)}".encode())
        except:
            pass
    
    finally:
        try:
            cliente.close()
        except:
            pass
        print(f"🔌 Cliente {addr} desconectado\n")


# Iniciar servidor
print("="*60)
print("🚀 SERVIDOR SOCIALTEC")
print("="*60)

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PUERTO))
    server.listen(5)
    print(f"✅ Servidor iniciado en {IP}:{PUERTO}")
    print(f"📡 Esperando conexiones...")
    print("="*60 + "\n")

    while True:
        cliente, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(cliente, addr))
        hilo.daemon = True
        hilo.start()

except KeyboardInterrupt:
    print("\n" + "="*60)
    print("⛔ Servidor detenido por el usuario")
    print("="*60)
except Exception as e:
    print(f"\n❌ Error en el servidor: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        server.close()
    except:
        pass