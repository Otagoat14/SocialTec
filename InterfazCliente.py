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
            text="Confirmar contraseña:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        self.entry_password_confirm = tk.Entry(
            frame_form,
            font=('Arial', 12),
            width=40,
            show='●',
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_password_confirm.pack(pady=(0, 20))
        
        tk.Label(
            frame_form,
            text="Foto de perfil (opcional):",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))
        
        frame_foto = tk.Frame(frame_form, bg=self.colores['blanco'])
        frame_foto.pack(pady=(0, 20))
        
        self.entry_foto = tk.Entry(
            frame_foto,
            font=('Arial', 10),
            width=30,
            relief=tk.SOLID,
            borderwidth=1,
            state='disabled'
        )
        self.entry_foto.pack(side='left', padx=(0, 10))
        
        btn_seleccionar_foto = tk.Button(
            frame_foto,
            text="Seleccionar",
            font=('Arial', 10),
            bg=self.colores['gris'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.seleccionar_foto
        )
        btn_seleccionar_foto.pack(side='left')
        
        btn_registrar = tk.Button(
            frame_form,
            text="Registrarse",
            font=('Arial', 12, 'bold'),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            width=30,
            height=2,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.click_registrarse
        )
        btn_registrar.pack(pady=(10, 10))
        
        btn_volver = tk.Button(
            frame_form,
            text="Ya tengo una cuenta",
            font=('Arial', 11),
            bg=self.colores['gris'],
            fg=self.colores['blanco'],
            width=30,
            cursor='hand2',
            relief=tk.FLAT,
            command=self.mostrar_login
        )
        btn_volver.pack()


    def seleccionar_foto(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=(("Imágenes", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*"))
        )
        if filename:
            self.foto_perfil_path = filename
            self.entry_foto.config(state='normal')
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, os.path.basename(filename))
            self.entry_foto.config(state='disabled')


    def click_registrarse(self):
        nombre = self.entry_nombre_completo.get()
        usuario = self.entry_usuario_nuevo.get()
        password = self.entry_password_nuevo.get()
        password_confirm = self.entry_password_confirm.get()
        
        if not nombre or not usuario or not password:
            messagebox.showwarning("Advertencia", "Por favor complete los campos obligatorios")
            return
        
        if password != password_confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Advertencia", "La contraseña debe tener al menos 6 caracteres")
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(usuario)
            cliente.enviar(nombre)
            cliente.enviar("registro")
            cliente.enviar(password)
            cliente.enviar(self.foto_perfil_path if self.foto_perfil_path else "")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("REGISTRO_OK"):
                messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
                self.mostrar_login()
            else:
                messagebox.showerror("Error", "No se pudo crear la cuenta. El usuario puede ya existir.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {e}")

    
    #---------PANTALLA DE PERFIL-------------
    def mostrar_perfil(self):
        self.limpiar_ventana()
        
        frame_top = tk.Frame(self.root, bg=self.colores['primario'], height=60)
        frame_top.pack(fill='x')
        
        tk.Label(
            frame_top,
            text="Socialtec",
            font=('Arial', 20, 'bold'),
            fg=self.colores['blanco'],
            bg=self.colores['primario']
        ).pack(side='left', padx=20, pady=10)
        
        # Botón para ver solicitudes
        btn_solicitudes = tk.Button(
            frame_top,
            text="📬 Solicitudes",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_solicitudes
        )
        btn_solicitudes.pack(side='left', padx=10)
        
        btn_buscar = tk.Button(
            frame_top,
            text="🔍 Buscar Amigos",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_buscar
        )
        btn_buscar.pack(side='left', padx=10)
        
        btn_cerrar = tk.Button(
            frame_top,
            text="Cerrar Sesión",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_login
        )
        btn_cerrar.pack(side='right', padx=20)

        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        frame_perfil = tk.Frame(frame_principal, bg=self.colores['blanco'], relief=tk.SOLID, borderwidth=1)
        frame_perfil.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        canvas_foto = tk.Canvas(
            frame_perfil,
            width=150,
            height=150,
            bg=self.colores['gris'],
            highlightthickness=0
        )
        canvas_foto.pack(pady=20)
        canvas_foto.create_text(75, 75, text="👤", font=('Arial', 60))
        
        tk.Label(
            frame_perfil,
            text=self.usuario_actual or "Usuario",
            font=('Arial', 24, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=10)
        
        tk.Label(
            frame_perfil,
            text=self.nombre_completo or "Usuario",
            font=('Arial', 14),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        ).pack(pady=5)
        
        frame_amigos = tk.Frame(frame_principal, bg=self.colores['blanco'], relief=tk.SOLID, borderwidth=1)
        frame_amigos.pack(side='right', fill='both', expand=True)
        
        tk.Label(
            frame_amigos,
            text="Lista de Amigos",
            font=('Arial', 18, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=15)
        
        frame_scroll_amigos = tk.Frame(frame_amigos, bg=self.colores['blanco'])
        frame_scroll_amigos.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        canvas_amigos = tk.Canvas(frame_scroll_amigos, bg=self.colores['blanco'])
        scrollbar_amigos = ttk.Scrollbar(frame_scroll_amigos, orient="vertical", command=canvas_amigos.yview)
        self.frame_lista_amigos = tk.Frame(canvas_amigos, bg=self.colores['blanco'])

        self.frame_lista_amigos.bind(
            "<Configure>",
            lambda e: canvas_amigos.configure(scrollregion=canvas_amigos.bbox("all"))
        )

        canvas_amigos.create_window((0, 0), window=self.frame_lista_amigos, anchor="nw")
        canvas_amigos.configure(yscrollcommand=scrollbar_amigos.set)

        canvas_amigos.pack(side="left", fill="both", expand=True)
        scrollbar_amigos.pack(side="right", fill="y")
        
        # Cargar amigos desde el servidor
        self.cargar_amigos()


    def cargar_amigos(self):
        """Carga la lista de amigos desde el servidor"""
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar("")  # Dato vacío
            cliente.enviar("obtener_amigos")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("AMIGOS_OK"):
                datos = respuesta.split("|", 1)[1]
                amigos = json.loads(datos)
                
                # Ordenar amigos alfabéticamente por username
                amigos_ordenados = sorted(amigos, key=lambda x: x['username'].lower())
                
                # Limpiar lista anterior
                for widget in self.frame_lista_amigos.winfo_children():
                    widget.destroy()
                
                # Mostrar amigos
                if amigos_ordenados:
                    for amigo in amigos_ordenados:
                        self.mostrar_amigo_en_lista(amigo)
                else:
                    tk.Label(
                        self.frame_lista_amigos,
                        text="No tienes amigos aún",
                        font=('Arial', 12),
                        bg=self.colores['blanco'],
                        fg=self.colores['gris']
                    ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los amigos: {e}")


    def mostrar_amigo_en_lista(self, amigo):
        """Muestra un amigo en la lista"""
        frame_amigo = tk.Frame(
            self.frame_lista_amigos,
            bg=self.colores['fondo'],
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_amigo.pack(fill='x', padx=5, pady=5)
        
        tk.Label(
            frame_amigo,
            text=f"{amigo['username']} ({amigo['nombre']})",
            font=('Arial', 12),
            bg=self.colores['fondo']
        ).pack(side='left', padx=10, pady=10)
        
        btn_ver = tk.Button(
            frame_amigo,
            text="Ver Perfil",
            font=('Arial', 10),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.ver_perfil_amigo(amigo['username'])
        )
        btn_ver.pack(side='right', padx=5, pady=5)

    
    def ver_perfil_amigo(self, username):
        """Muestra el perfil de un amigo"""
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(username)
            cliente.enviar("")
            cliente.enviar("obtener_perfil")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("PERFIL_OK"):
                datos = respuesta.split("|", 1)[1]
                perfil = json.loads(datos)
                
                # Crear ventana de perfil
                ventana_perfil = tk.Toplevel(self.root)
                ventana_perfil.title(f"Perfil de {perfil['username']}")
                ventana_perfil.geometry("400x300")
                ventana_perfil.configure(bg=self.colores['fondo'])
                
                tk.Label(
                    ventana_perfil,
                    text=perfil['username'],
                    font=('Arial', 24, 'bold'),
                    bg=self.colores['fondo']
                ).pack(pady=20)
                
                tk.Label(
                    ventana_perfil,
                    text=perfil['nombre'],
                    font=('Arial', 16),
                    bg=self.colores['fondo']
                ).pack(pady=10)
                
                # Botón para eliminar amistad
                btn_eliminar = tk.Button(
                    ventana_perfil,
                    text="Eliminar Amistad",
                    font=('Arial', 12),
                    bg='#dc3545',
                    fg=self.colores['blanco'],
                    cursor='hand2',
                    command=lambda: self.eliminar_amistad_desde_perfil(username, ventana_perfil)
                )
                btn_eliminar.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el perfil: {e}")


    def eliminar_amistad_desde_perfil(self, username_amigo, ventana):
        """Elimina una amistad"""
        respuesta_conf = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar la amistad con {username_amigo}?"
        )
        
        if not respuesta_conf:
            return
        
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(self.usuario_actual)
            cliente.enviar(username_amigo)
            cliente.enviar("eliminar_amistad")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("ELIMINAR_OK"):
                messagebox.showinfo("Éxito", "Amistad eliminada")
                ventana.destroy()
                self.mostrar_perfil()  # Recargar perfil
            else:
                messagebox.showerror("Error", "No se pudo eliminar la amistad")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    
    #---------PANTALLA DE SOLICITUDES-------------
    def mostrar_solicitudes(self):
        self.limpiar_ventana()
        
        frame_top = tk.Frame(self.root, bg=self.colores['primario'], height=60)
        frame_top.pack(fill='x')
        
        tk.Label(
            frame_top,
            text="Socialtec",
            font=('Arial', 20, 'bold'),
            fg=self.colores['blanco'],
            bg=self.colores['primario']
        ).pack(side='left', padx=20, pady=10)
        
        btn_volver = tk.Button(
            frame_top,
            text="← Volver al Perfil",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_perfil
        )
        btn_volver.pack(side='left', padx=10)
        
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            frame_principal,
            text="Solicitudes de Amistad",
            font=('Arial', 24, 'bold'),
            bg=self.colores['fondo']
        ).pack(pady=20)
        
        frame_resultados = tk.Frame(frame_principal, bg=self.colores['blanco'])
        frame_resultados.pack(fill='both', expand=True)
        
        frame_scroll = tk.Frame(frame_resultados, bg=self.colores['blanco'])
        frame_scroll.pack(fill='both', expand=True, padx=10, pady=10)

        canvas_resultados = tk.Canvas(frame_scroll, bg=self.colores['blanco'])
        scrollbar_resultados = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_resultados.yview)
        self.frame_lista_solicitudes = tk.Frame(canvas_resultados, bg=self.colores['blanco'])

        self.frame_lista_solicitudes.bind(
            "<Configure>",
            lambda e: canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all"))
        )

        canvas_resultados.create_window((0, 0), window=self.frame_lista_solicitudes, anchor="nw")
        canvas_resultados.configure(yscrollcommand=scrollbar_resultados.set)

        canvas_resultados.pack(side="left", fill="both", expand=True)
        scrollbar_resultados.pack(side="right", fill="y")
        
        # Cargar solicitudes
        self.cargar_solicitudes()


    def cargar_solicitudes(self):
        """Carga las solicitudes pendientes"""
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
                
                # Limpiar lista
                for widget in self.frame_lista_solicitudes.winfo_children():
                    widget.destroy()
                
                if solicitudes:
                    for solicitud in solicitudes:
                        self.mostrar_solicitud(solicitud)
                else:
                    tk.Label(
                        self.frame_lista_solicitudes,
                        text="No tienes solicitudes pendientes",
                        font=('Arial', 12),
                        bg=self.colores['blanco'],
                        fg=self.colores['gris']
                    ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las solicitudes: {e}")


    def mostrar_solicitud(self, solicitud):
        """Muestra una solicitud en la lista"""
        frame_solicitud = tk.Frame(
            self.frame_lista_solicitudes,
            bg=self.colores['fondo'],
            relief=tk.SOLID,
            borderwidth=1
        )
        frame_solicitud.pack(fill='x', padx=5, pady=5)
        
        tk.Label(
            frame_solicitud,
            text=f"{solicitud['username']} quiere ser tu amigo",
            font=('Arial', 12),
            bg=self.colores['fondo']
        ).pack(side='left', padx=10, pady=10)
        
        btn_rechazar = tk.Button(
            frame_solicitud,
            text="Rechazar",
            font=('Arial', 10),
            bg='#dc3545',
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.rechazar_solicitud(solicitud['id'])
        )
        btn_rechazar.pack(side='right', padx=5, pady=5)
        
        btn_aceptar = tk.Button(
            frame_solicitud,
            text="Aceptar",
            font=('Arial', 10),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=lambda: self.aceptar_solicitud(solicitud['id'], solicitud['username'])
        )
        btn_aceptar.pack(side='right', padx=5, pady=5)


    def aceptar_solicitud(self, solicitud_id, username_remitente):
        """Acepta una solicitud de amistad"""
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(str(solicitud_id))
            cliente.enviar(self.usuario_actual)
            cliente.enviar("aceptar_solicitud")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("ACEPTAR_OK"):
                messagebox.showinfo("Éxito", f"Ahora eres amigo de {username_remitente}")
                self.cargar_solicitudes()  # Recargar solicitudes
            else:
                messagebox.showerror("Error", "No se pudo aceptar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    def rechazar_solicitud(self, solicitud_id):
        """Rechaza una solicitud de amistad"""
        try:
            cliente = ClienteTCP()
            cliente.conectar(IP, PUERTO)
            cliente.enviar(str(solicitud_id))
            cliente.enviar("")
            cliente.enviar("rechazar_solicitud")
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and respuesta.startswith("RECHAZAR_OK"):
                messagebox.showinfo("Éxito", "Solicitud rechazada")
                self.cargar_solicitudes()  # Recargar solicitudes
            else:
                messagebox.showerror("Error", "No se pudo rechazar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    #---------PANTALLA DE BUSQUEDA-------------
    def mostrar_buscar(self):
        self.limpiar_ventana()
        
        frame_top = tk.Frame(self.root, bg=self.colores['primario'], height=60)
        frame_top.pack(fill='x')
        
        tk.Label(
            frame_top,
            text="Socialtec",
            font=('Arial', 20, 'bold'),
            fg=self.colores['blanco'],
            bg=self.colores['primario']
        ).pack(side='left', padx=20, pady=10)
        
        btn_volver = tk.Button(
            frame_top,
            text="← Volver al Perfil",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_perfil
        )
        btn_volver.pack(side='left', padx=10)
        
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
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
            text="🔍 Buscar",
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
        """Busca personas en la base de datos"""
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
                
                # Limpiar resultados anteriores
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
        """Muestra un resultado de búsqueda"""
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

        # Si es amigo, mostrar botón de eliminar
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
                text="✓ Amigo",
                font=('Arial', 10),
                bg=self.colores['fondo'],
                fg=self.colores['secundario']
            ).pack(side='right', padx=10)

        # Si no es amigo, mostrar botón de agregar
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
        """Elimina una amistad"""
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
                self.click_buscar_persona()  # Recargar búsqueda
            else:
                messagebox.showerror("Error", "No se pudo eliminar la amistad")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    def click_agregar_amistad(self, resultado):
        """Envía solicitud de amistad"""
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
                self.click_buscar_persona()  # Recargar búsqueda
            else:
                messagebox.showerror("Error", "No se pudo enviar la solicitud")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialtecCliente(root)
    root.mainloop()