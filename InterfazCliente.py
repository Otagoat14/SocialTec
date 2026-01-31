import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import json
from Registro import ManejoUsuarios
from Cliente_Prueba import ClienteTCP
from Merge_Sort import amigos_ordenados

IP = "127.0.0.1"
PUERTO = 5001


class SocialtecCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Socialtec - Red Social")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.usuario_actual = None
        self.user_id = None
        self.nombre_completo = None
        self.foto_perfil_path = None
        self.configurar_estilo()
        self.registro = ManejoUsuarios()
        self.mostrar_login()
    
    def configurar_estilo(self):
        self.colores = {
            'primario': '#1877f2',
            'secundario': '#42b72a',
            'fondo': '#f0f2f5',
            'blanco': '#ffffff',
            'texto': '#050505',
            'gris': '#65676b'
        }
        self.root.configure(bg=self.colores['fondo'])
    
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ========== FUNCIONES AUXILIARES PARA IMÁGENES ==========
    
    def cargar_imagen_perfil(self, ruta_imagen, tamaño=(150, 150)):
        """
        Carga una imagen de perfil desde una ruta y la redimensiona.
        Si la ruta no existe o es None, retorna una imagen por defecto.
        """
        try:
            if ruta_imagen and os.path.exists(ruta_imagen):
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize(tamaño, Image.Resampling.LANCZOS)
                
                # Crear máscara circular
                mask = Image.new('L', tamaño, 0)
                from PIL import ImageDraw
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + tamaño, fill=255)
                
                # Aplicar máscara
                output = Image.new('RGBA', tamaño, (0, 0, 0, 0))
                output.paste(imagen, (0, 0))
                output.putalpha(mask)
                
                return ImageTk.PhotoImage(output)
            else:
                # Imagen por defecto
                return self.crear_imagen_default(tamaño)
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return self.crear_imagen_default(tamaño)
    
    def crear_imagen_default(self, tamaño=(150, 150)):
        """Crea una imagen de perfil por defecto (círculo gris con iniciales)"""
        from PIL import ImageDraw
        
        imagen = Image.new('RGB', tamaño, color='#e0e0e0')
        draw = ImageDraw.Draw(imagen)
        
        # Dibujar círculo
        draw.ellipse((0, 0, tamaño[0]-1, tamaño[1]-1), fill='#90caf9', outline='#1877f2', width=3)
        
        # Agregar icono de usuario (símbolo simple)
        center_x, center_y = tamaño[0] // 2, tamaño[1] // 2
        # Cabeza
        head_radius = tamaño[0] // 6
        draw.ellipse(
            (center_x - head_radius, center_y - tamaño[1]//4 - head_radius,
             center_x + head_radius, center_y - tamaño[1]//4 + head_radius),
            fill='#ffffff'
        )
        # Cuerpo
        body_width = tamaño[0] // 3
        body_height = tamaño[1] // 3
        draw.ellipse(
            (center_x - body_width, center_y,
             center_x + body_width, center_y + body_height * 2),
            fill='#ffffff'
        )
        
        return ImageTk.PhotoImage(imagen)


    #----------INICIO PANTALLA LOGIN---------------
    def mostrar_login(self):
        self.limpiar_ventana()
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.place(relx=0.5, rely=0.5, anchor='center')

        titulo = tk.Label(
            frame_principal,
            text="Socialtec",
            font=('Arial', 36, 'bold'),
            fg=self.colores['primario'],
            bg=self.colores['fondo']
        )
        titulo.pack(pady=20)

        frame_login = tk.Frame(frame_principal, bg=self.colores['blanco'], padx=30, pady=30)
        frame_login.pack(pady=10)
        
        tk.Label(
            frame_login,
            text="Usuario:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_usuario_login = tk.Entry(
            frame_login,
            font=('Arial', 12),
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_usuario_login.pack(pady=(0, 15))

        tk.Label(
            frame_login,
            text="Contraseña:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_password_login = tk.Entry(
            frame_login,
            font=('Arial', 12),
            width=30,
            show='●',
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_password_login.pack(pady=(0, 20))
   
        btn_login = tk.Button(
            frame_login,
            text="Iniciar Sesión",
            font=('Arial', 12, 'bold'),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            width=25,
            height=2,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.click_iniciar_sesion
        )
        btn_login.pack(pady=(0, 10))
        
        btn_crear = tk.Button(
            frame_login,
            text="Crear nueva cuenta",
            font=('Arial', 11),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            width=25,
            height=1,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.mostrar_crear_cuenta
        )
        btn_crear.pack()


    def click_iniciar_sesion(self):
        usuario = self.entry_usuario_login.get()
        contra = self.entry_password_login.get()
        
        if not usuario or not contra:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(usuario)
            cliente.enviar(contra)
            cliente.enviar("login")
            
            respuesta = cliente.recibir()
            cliente.cerrar()

            if respuesta and respuesta.startswith("LOGIN_OK"):
                partes = respuesta.split("|")
                self.user_id = partes[1]
                self.nombre_completo = partes[2]
                self.foto_perfil_path = partes[3] if len(partes) > 3 and partes[3] else None
                self.usuario_actual = usuario
                self.mostrar_perfil()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")

    
    # ---------INICIO PAGINA REGISTRO---------------
    def mostrar_crear_cuenta(self):
        self.limpiar_ventana()
        
        canvas = tk.Canvas(self.root, bg=self.colores['fondo'])
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=self.colores['fondo'])
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((400, 0), window=frame_scroll, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        titulo = tk.Label(
            frame_scroll,
            text="Crear Nueva Cuenta",
            font=('Arial', 28, 'bold'),
            fg=self.colores['primario'],
            bg=self.colores['fondo']
        )
        titulo.pack(pady=30)
        
        frame_form = tk.Frame(frame_scroll, bg=self.colores['blanco'], padx=40, pady=30)
        frame_form.pack(padx=50)
        
        tk.Label(
            frame_form,
            text="Nombre completo:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_nombre_completo = tk.Entry(
            frame_form,
            font=('Arial', 12),
            width=40,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_nombre_completo.pack(pady=(0, 15))
        
        tk.Label(
            frame_form,
            text="Usuario:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_usuario_nuevo = tk.Entry(
            frame_form,
            font=('Arial', 12),
            width=40,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_usuario_nuevo.pack(pady=(0, 15))
        
        tk.Label(
            frame_form,
            text="Contraseña:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_password_nuevo = tk.Entry(
            frame_form,
            font=('Arial', 12),
            width=40,
            show='●',
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_password_nuevo.pack(pady=(0, 15))
        
        tk.Label(
            frame_form,
            text="Foto de Perfil (opcional):",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        frame_foto = tk.Frame(frame_form, bg=self.colores['blanco'])
        frame_foto.pack(pady=(0, 15))
        
        self.label_ruta_foto = tk.Label(
            frame_foto,
            text="Ninguna imagen seleccionada",
            font=('Arial', 10),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        )
        self.label_ruta_foto.pack(side='left', padx=(0, 10))
        
        btn_seleccionar_foto = tk.Button(
            frame_foto,
            text="Seleccionar Imagen",
            font=('Arial', 10),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.seleccionar_foto
        )
        btn_seleccionar_foto.pack(side='left')
        
        self.ruta_foto_seleccionada = None
        
        btn_registrar = tk.Button(
            frame_form,
            text="Registrarse",
            font=('Arial', 12, 'bold'),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            width=35,
            height=2,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.click_registrar
        )
        btn_registrar.pack(pady=(10, 20))
        
        btn_volver = tk.Button(
            frame_form,
            text="← Volver al inicio de sesión",
            font=('Arial', 11),
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            cursor='hand2',
            relief=tk.FLAT,
            command=self.mostrar_login
        )
        btn_volver.pack()

    
    def seleccionar_foto(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if ruta:
            self.ruta_foto_seleccionada = ruta
            nombre_archivo = os.path.basename(ruta)
            self.label_ruta_foto.config(
                text=f"Seleccionado: {nombre_archivo}",
                fg=self.colores['secundario']
            )

    
    def click_registrar(self):
        nombre = self.entry_nombre_completo.get()
        usuario = self.entry_usuario_nuevo.get()
        contra = self.entry_password_nuevo.get()
        foto = self.ruta_foto_seleccionada
        
        if not nombre or not usuario or not contra:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos obligatorios")
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(usuario)
            cliente.enviar(nombre)
            cliente.enviar("registro")
            cliente.enviar(contra)
            cliente.enviar(foto if foto else "")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("REGISTRO_OK"):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.mostrar_login()
            else:
                mensaje_error = respuesta.split("|")[1] if "|" in respuesta else "Error al registrar"
                messagebox.showerror("Error", mensaje_error)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")


    # ---------INICIO PAGINA PERFIL---------------
    def mostrar_perfil(self):
        self.limpiar_ventana()
        
        barra_superior = tk.Frame(self.root, bg=self.colores['primario'], height=60)
        barra_superior.pack(fill='x')
        
        tk.Label(
            barra_superior,
            text="Socialtec",
            font=('Arial', 20, 'bold'),
            fg=self.colores['blanco'],
            bg=self.colores['primario']
        ).pack(side='left', padx=20)
        
        btn_cerrar_sesion = tk.Button(
            barra_superior,
            text="Cerrar Sesión",
            font=('Arial', 11),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.mostrar_login
        )
        btn_cerrar_sesion.pack(side='right', padx=20)
        
        frame_pestañas = ttk.Notebook(self.root)
        frame_pestañas.pack(fill='both', expand=True)
        
        pestaña_perfil = tk.Frame(frame_pestañas, bg=self.colores['fondo'])
        pestaña_amigos = tk.Frame(frame_pestañas, bg=self.colores['fondo'])
        pestaña_solicitudes = tk.Frame(frame_pestañas, bg=self.colores['fondo'])
        pestaña_buscar = tk.Frame(frame_pestañas, bg=self.colores['fondo'])
        
        frame_pestañas.add(pestaña_perfil, text="Mi Perfil")
        frame_pestañas.add(pestaña_amigos, text="Mis Amigos")
        frame_pestañas.add(pestaña_solicitudes, text="Solicitudes")
        frame_pestañas.add(pestaña_buscar, text="Buscar Personas")
        
        self.crear_contenido_perfil(pestaña_perfil)
        self.crear_contenido_amigos(pestaña_amigos)
        self.crear_contenido_solicitudes(pestaña_solicitudes)
        self.crear_contenido_buscar(pestaña_buscar)

    
    def crear_contenido_perfil(self, parent):
        frame_principal = tk.Frame(parent, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        frame_info = tk.Frame(frame_principal, bg=self.colores['blanco'], padx=40, pady=40)
        frame_info.pack(fill='both', expand=True)
        
        # ========== CARGAR Y MOSTRAR FOTO DE PERFIL ==========
        foto_perfil = self.cargar_imagen_perfil(self.foto_perfil_path, tamaño=(150, 150))
        
        label_foto = tk.Label(
            frame_info,
            image=foto_perfil,
            bg=self.colores['blanco']
        )
        label_foto.image = foto_perfil  # Mantener referencia
        label_foto.pack(pady=(0, 20))
        
        tk.Label(
            frame_info,
            text=self.nombre_completo,
            font=('Arial', 24, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=(0, 10))
        
        tk.Label(
            frame_info,
            text=f"@{self.usuario_actual}",
            font=('Arial', 16),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        ).pack(pady=(0, 30))
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar("")
            cliente.enviar("obtener_amigos")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("AMIGOS_OK"):
                datos = respuesta.split("|", 1)[1]
                amigos = json.loads(datos)
                cantidad_amigos = len(amigos)
            else:
                cantidad_amigos = 0
        except:
            cantidad_amigos = 0
        
        frame_stats = tk.Frame(frame_info, bg=self.colores['fondo'])
        frame_stats.pack(pady=20)
        
        tk.Label(
            frame_stats,
            text=str(cantidad_amigos),
            font=('Arial', 32, 'bold'),
            bg=self.colores['fondo'],
            fg=self.colores['primario']
        ).pack()
        
        tk.Label(
            frame_stats,
            text="Amigos",
            font=('Arial', 14),
            bg=self.colores['fondo'],
            fg=self.colores['gris']
        ).pack()

    
    def crear_contenido_amigos(self, parent):
        frame_principal = tk.Frame(parent, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_principal,
            text="Mis Amigos",
            font=('Arial', 24, 'bold'),
            bg=self.colores['fondo']
        ).pack(pady=20)
        
        frame_botones = tk.Frame(frame_principal, bg=self.colores['fondo'])
        frame_botones.pack(pady=10)
        
        btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar Lista",
            font=('Arial', 11),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.cargar_lista_amigos()
        )
        btn_actualizar.pack(side='left', padx=5)
        
        btn_ordenar = tk.Button(
            frame_botones,
            text="Ordenar Alfabéticamente",
            font=('Arial', 11),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.ordenar_amigos
        )
        btn_ordenar.pack(side='left', padx=5)
        
        frame_lista = tk.Frame(frame_principal, bg=self.colores['blanco'])
        frame_lista.pack(fill='both', expand=True, pady=(10, 0))
        
        canvas_amigos = tk.Canvas(frame_lista, bg=self.colores['blanco'])
        scrollbar_amigos = ttk.Scrollbar(frame_lista, orient="vertical", command=canvas_amigos.yview)
        self.frame_lista_amigos = tk.Frame(canvas_amigos, bg=self.colores['blanco'])
        
        self.frame_lista_amigos.bind(
            "<Configure>",
            lambda e: canvas_amigos.configure(scrollregion=canvas_amigos.bbox("all"))
        )
        
        canvas_amigos.create_window((0, 0), window=self.frame_lista_amigos, anchor="nw")
        canvas_amigos.configure(yscrollcommand=scrollbar_amigos.set)
        
        canvas_amigos.pack(side="left", fill="both", expand=True)
        scrollbar_amigos.pack(side="right", fill="y")
        
        self.cargar_lista_amigos()

    
    def cargar_lista_amigos(self):
        for widget in self.frame_lista_amigos.winfo_children():
            widget.destroy()
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar("")
            cliente.enviar("obtener_amigos")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("AMIGOS_OK"):
                datos = respuesta.split("|", 1)[1]
                amigos = json.loads(datos)
                
                if amigos:
                    for amigo in amigos:
                        self.mostrar_tarjeta_amigo(amigo)
                else:
                    tk.Label(
                        self.frame_lista_amigos,
                        text="Aún no tienes amigos. ¡Busca personas para agregar!",
                        font=('Arial', 12),
                        bg=self.colores['blanco'],
                        fg=self.colores['gris']
                    ).pack(pady=50)
            else:
                messagebox.showerror("Error", "No se pudieron cargar los amigos")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar amigos: {e}")

    
    def mostrar_tarjeta_amigo(self, amigo):
        frame_amigo = tk.Frame(
            self.frame_lista_amigos,
            bg=self.colores['fondo'],
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_amigo.pack(fill='x', padx=10, pady=5)
        
        # ========== CARGAR FOTO DEL AMIGO ==========
        foto_amigo = self.cargar_imagen_perfil(amigo.get('foto'), tamaño=(60, 60))
        
        label_foto = tk.Label(
            frame_amigo,
            image=foto_amigo,
            bg=self.colores['fondo']
        )
        label_foto.image = foto_amigo  # Mantener referencia
        label_foto.pack(side='left', padx=10, pady=10)
        
        frame_info = tk.Frame(frame_amigo, bg=self.colores['fondo'])
        frame_info.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(
            frame_info,
            text=amigo['nombre'],
            font=('Arial', 14, 'bold'),
            bg=self.colores['fondo']
        ).pack(anchor='w')
        
        tk.Label(
            frame_info,
            text=f"@{amigo['username']}",
            font=('Arial', 11),
            bg=self.colores['fondo'],
            fg=self.colores['gris']
        ).pack(anchor='w')
        
        btn_ver_perfil = tk.Button(
            frame_amigo,
            text="Ver Perfil",
            font=('Arial', 10),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.ver_perfil_amigo(amigo['username'])
        )
        btn_ver_perfil.pack(side='right', padx=5, pady=5)
        
        btn_eliminar = tk.Button(
            frame_amigo,
            text="Eliminar",
            font=('Arial', 10),
            bg='#dc3545',
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.click_eliminar_amigo(amigo)
        )
        btn_eliminar.pack(side='right', padx=5, pady=5)

    
    def ordenar_amigos(self):
        try:
            amigos_ordenados_list = amigos_ordenados(self.usuario_actual)
            
            for widget in self.frame_lista_amigos.winfo_children():
                widget.destroy()
            
            for username_amigo in amigos_ordenados_list:
                try:
                    cliente = ClienteTCP()
                    cliente.conectar(IP, PUERTO)
                    cliente.enviar(username_amigo)
                    cliente.enviar("")
                    cliente.enviar("obtener_perfil")
                    
                    respuesta = cliente.recibir()
                    cliente.cerrar()
                    
                    if respuesta and respuesta.startswith("PERFIL_OK"):
                        datos = respuesta.split("|", 1)[1]
                        perfil = json.loads(datos)
                        
                        amigo_data = {
                            'id': perfil['id'],
                            'username': perfil['username'],
                            'nombre': perfil['nombre'],
                            'foto': perfil.get('foto', ''),
                            'fecha': ''
                        }
                        
                        self.mostrar_tarjeta_amigo(amigo_data)
                except:
                    continue
            
            messagebox.showinfo("Éxito", "Lista de amigos ordenada alfabéticamente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al ordenar: {e}")

    
    def click_eliminar_amigo(self, amigo):
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar a {amigo['nombre']} de sus amigos?"
        )
        
        if not respuesta:
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar(amigo['username'])
            cliente.enviar("eliminar_amistad")
            
            respuesta_srv = cliente.recibir()
            cliente.cerrar()
            
            if respuesta_srv and respuesta_srv.startswith("ELIMINAR_OK"):
                messagebox.showinfo("Éxito", f"Amistad con {amigo['nombre']} eliminada")
                self.cargar_lista_amigos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la amistad")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    
    def ver_perfil_amigo(self, username_amigo):
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(username_amigo)
            cliente.enviar("")
            cliente.enviar("obtener_perfil")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("PERFIL_OK"):
                datos = respuesta.split("|", 1)[1]
                perfil = json.loads(datos)
                self.mostrar_ventana_perfil_amigo(perfil)
            else:
                messagebox.showerror("Error", "No se pudo cargar el perfil")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    
    def mostrar_ventana_perfil_amigo(self, perfil):
        ventana_perfil = tk.Toplevel(self.root)
        ventana_perfil.title(f"Perfil de {perfil['username']}")
        ventana_perfil.geometry("500x600")
        ventana_perfil.configure(bg=self.colores['fondo'])
        ventana_perfil.resizable(False, False)
        
        frame_contenido = tk.Frame(ventana_perfil, bg=self.colores['blanco'], padx=40, pady=40)
        frame_contenido.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ========== CARGAR Y MOSTRAR FOTO DEL AMIGO ==========
        foto_amigo = self.cargar_imagen_perfil(perfil.get('foto'), tamaño=(200, 200))
        
        label_foto = tk.Label(
            frame_contenido,
            image=foto_amigo,
            bg=self.colores['blanco']
        )
        label_foto.image = foto_amigo  # Mantener referencia
        label_foto.pack(pady=(0, 30))
        
        tk.Label(
            frame_contenido,
            text=perfil['nombre'],
            font=('Arial', 28, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=(0, 10))
        
        tk.Label(
            frame_contenido,
            text=f"@{perfil['username']}",
            font=('Arial', 18),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        ).pack(pady=(0, 40))
        
        btn_cerrar = tk.Button(
            frame_contenido,
            text="Cerrar",
            font=('Arial', 12),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            width=20,
            command=ventana_perfil.destroy
        )
        btn_cerrar.pack(pady=20)

    
    def crear_contenido_solicitudes(self, parent):
        frame_principal = tk.Frame(parent, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_principal,
            text="Solicitudes de Amistad",
            font=('Arial', 24, 'bold'),
            bg=self.colores['fondo']
        ).pack(pady=20)
        
        btn_actualizar = tk.Button(
            frame_principal,
            text="Actualizar Solicitudes",
            font=('Arial', 11),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.cargar_solicitudes
        )
        btn_actualizar.pack(pady=10)
        
        frame_lista = tk.Frame(frame_principal, bg=self.colores['blanco'])
        frame_lista.pack(fill='both', expand=True, pady=(10, 0))
        
        canvas_solicitudes = tk.Canvas(frame_lista, bg=self.colores['blanco'])
        scrollbar_solicitudes = ttk.Scrollbar(frame_lista, orient="vertical", command=canvas_solicitudes.yview)
        self.frame_lista_solicitudes = tk.Frame(canvas_solicitudes, bg=self.colores['blanco'])
        
        self.frame_lista_solicitudes.bind(
            "<Configure>",
            lambda e: canvas_solicitudes.configure(scrollregion=canvas_solicitudes.bbox("all"))
        )
        
        canvas_solicitudes.create_window((0, 0), window=self.frame_lista_solicitudes, anchor="nw")
        canvas_solicitudes.configure(yscrollcommand=scrollbar_solicitudes.set)
        
        canvas_solicitudes.pack(side="left", fill="both", expand=True)
        scrollbar_solicitudes.pack(side="right", fill="y")
        
        self.cargar_solicitudes()

    
    def cargar_solicitudes(self):
        for widget in self.frame_lista_solicitudes.winfo_children():
            widget.destroy()
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar("")
            cliente.enviar("obtener_solicitudes")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("SOLICITUDES_OK"):
                datos = respuesta.split("|", 1)[1]
                solicitudes = json.loads(datos)
                
                if solicitudes:
                    for solicitud in solicitudes:
                        self.mostrar_tarjeta_solicitud(solicitud)
                else:
                    tk.Label(
                        self.frame_lista_solicitudes,
                        text="No tienes solicitudes pendientes",
                        font=('Arial', 12),
                        bg=self.colores['blanco'],
                        fg=self.colores['gris']
                    ).pack(pady=50)
            else:
                messagebox.showerror("Error", "No se pudieron cargar las solicitudes")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar solicitudes: {e}")

    
    def mostrar_tarjeta_solicitud(self, solicitud):
        frame_solicitud = tk.Frame(
            self.frame_lista_solicitudes,
            bg=self.colores['fondo'],
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_solicitud.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            frame_solicitud,
            text=f"@{solicitud['username']}",
            font=('Arial', 14, 'bold'),
            bg=self.colores['fondo']
        ).pack(side='left', padx=20, pady=15)
        
        btn_rechazar = tk.Button(
            frame_solicitud,
            text="Rechazar",
            font=('Arial', 10),
            bg='#dc3545',
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.click_rechazar_solicitud(solicitud)
        )
        btn_rechazar.pack(side='right', padx=5, pady=5)
        
        btn_aceptar = tk.Button(
            frame_solicitud,
            text="Aceptar",
            font=('Arial', 10),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.click_aceptar_solicitud(solicitud)
        )
        btn_aceptar.pack(side='right', padx=5, pady=5)

    
    def click_aceptar_solicitud(self, solicitud):
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(str(solicitud['id']))
            cliente.enviar(self.usuario_actual)
            cliente.enviar("aceptar_solicitud")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("ACEPTAR_OK"):
                messagebox.showinfo("Éxito", f"Ahora eres amigo de {solicitud['username']}")
                self.cargar_solicitudes()
            else:
                messagebox.showerror("Error", "No se pudo aceptar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    
    def click_rechazar_solicitud(self, solicitud):
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(str(solicitud['id']))
            cliente.enviar("")
            cliente.enviar("rechazar_solicitud")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("RECHAZAR_OK"):
                messagebox.showinfo("Info", f"Solicitud de {solicitud['username']} rechazada")
                self.cargar_solicitudes()
            else:
                messagebox.showerror("Error", "No se pudo rechazar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    
    def crear_contenido_buscar(self, parent):
        frame_principal = tk.Frame(parent, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_principal,
            text="Buscar Personas",
            font=('Arial', 24, 'bold'),
            bg=self.colores['fondo']
        ).pack(pady=20)
        
        frame_busqueda = tk.Frame(frame_principal, bg=self.colores['blanco'], padx=30, pady=20)
        frame_busqueda.pack(fill='x')
        
        tk.Label(
            frame_busqueda,
            text="Usuario:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(side='left', padx=(0, 10))
        
        self.entry_buscar_usuario = tk.Entry(
            frame_busqueda,
            font=('Arial', 12),
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_buscar_usuario.pack(side='left', padx=(0, 20))
        
        btn_buscar = tk.Button(
            frame_busqueda,
            text="Buscar",
            font=('Arial', 12, 'bold'),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.click_buscar_persona
        )
        btn_buscar.pack(side='left')
        
        frame_resultados = tk.Frame(frame_principal, bg=self.colores['blanco'])
        frame_resultados.pack(fill='both', expand=True, pady=(20, 0))

        tk.Label(
            frame_resultados,
            text="Resultados de Búsqueda",
            font=('Arial', 16, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=15)
        
        frame_scroll = tk.Frame(frame_resultados, bg=self.colores['blanco'])
        frame_scroll.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        canvas_resultados = tk.Canvas(frame_scroll, bg=self.colores['blanco'])
        scrollbar_resultados = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_resultados.yview)
        self.frame_lista_resultados = tk.Frame(canvas_resultados, bg=self.colores['blanco'])

        self.frame_lista_resultados.bind(
            "<Configure>",
            lambda e: canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all"))
        )

        canvas_resultados.create_window((0, 0), window=self.frame_lista_resultados, anchor="nw")
        canvas_resultados.configure(yscrollcommand=scrollbar_resultados.set)

        canvas_resultados.pack(side="left", fill="both", expand=True)
        scrollbar_resultados.pack(side="right", fill="y")

    
    def click_buscar_persona(self):
        termino = self.entry_buscar_usuario.get()
        
        if not termino:
            messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(termino)
            cliente.enviar(self.usuario_actual)
            cliente.enviar("buscar_usuarios")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("BUSCAR_OK"):
                datos = respuesta.split("|", 1)[1]
                resultados = json.loads(datos)
                
                for widget in self.frame_lista_resultados.winfo_children():
                    widget.destroy()
                
                if resultados:
                    for resultado in resultados:
                        self.mostrar_resultado_busqueda(resultado)
                else:
                    tk.Label(
                        self.frame_lista_resultados,
                        text="No se encontraron resultados",
                        font=('Arial', 12),
                        bg=self.colores['blanco'],
                        fg=self.colores['gris']
                    ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {e}")


    def mostrar_resultado_busqueda(self, resultado):
        frame_resultado = tk.Frame(
            self.frame_lista_resultados,
            bg=self.colores['fondo'],
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_resultado.pack(fill='x', padx=5, pady=5)

        tk.Label(
            frame_resultado,
            text=resultado['username'],
            font=('Arial', 14),
            bg=self.colores['fondo']
        ).pack(side='left', padx=20, pady=15)

        btn_ver = tk.Button(
            frame_resultado,
            text="Ver Perfil",
            font=('Arial', 10),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.ver_perfil_amigo(resultado['username'])
        )
        btn_ver.pack(side='right', padx=5, pady=5)

        if resultado['es_amigo']:
            btn_eliminar = tk.Button(
                frame_resultado,
                text="Eliminar Amistad",
                font=('Arial', 10),
                bg='#dc3545',
                fg=self.colores['blanco'],
                cursor='hand2',
                command=lambda: self.click_eliminar_amistad(resultado)
            )
            btn_eliminar.pack(side='right', padx=5, pady=5)

            tk.Label(
                frame_resultado,
                text="Amigo",
                font=('Arial', 10),
                bg=self.colores['fondo'],
                fg=self.colores['secundario']
            ).pack(side='right', padx=10)

        else:
            btn_agregar = tk.Button(
                frame_resultado,
                text="Enviar Solicitud",
                font=('Arial', 10),
                bg=self.colores['secundario'],
                fg=self.colores['blanco'],
                cursor='hand2',
                command=lambda: self.click_agregar_amistad(resultado)
            )
            btn_agregar.pack(side='right', padx=5, pady=5)


    def click_eliminar_amistad(self, resultado):
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar la amistad con {resultado['username']}?"
        )
        
        if not respuesta:
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar(resultado['username'])
            cliente.enviar("eliminar_amistad")
            
            respuesta_srv = cliente.recibir()
            cliente.cerrar()
            
            if respuesta_srv and respuesta_srv.startswith("ELIMINAR_OK"):
                messagebox.showinfo("Éxito", f"Amistad con {resultado['username']} eliminada")
                self.click_buscar_persona() 
            else:
                messagebox.showerror("Error", "No se pudo eliminar la amistad")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    def click_agregar_amistad(self, resultado):
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Desea enviar solicitud de amistad a {resultado['username']}?"
        )

        if not respuesta:
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar(resultado['username'])
            cliente.enviar("enviar_solicitud")
            
            respuesta_srv = cliente.recibir()
            cliente.cerrar()
            
            if respuesta_srv and respuesta_srv.startswith("SOLICITUD_OK"):
                messagebox.showinfo("Éxito", f"Solicitud enviada a {resultado['username']}")
                self.click_buscar_persona()  
            else:
                messagebox.showerror("Error", "No se pudo enviar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialtecCliente(root)
    root.mainloop()