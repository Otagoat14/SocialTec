import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import threading
from Registro import ManejoUsuarios
from Cliente_Prueba import *

ip = "127.0.0.1"
puerto = 5000


class SocialtecCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Socialtec - Red Social")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.usuario_actual = None
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

        # Deshabilitar botón mientras procesa
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Frame):
                        for b in btn.winfo_children():
                            if isinstance(b, tk.Button):
                                b.config(state='disabled')

        # Ejecutar login en un hilo separado
        threading.Thread(target=self._realizar_login, args=(usuario, contra), daemon=True).start()

    def _realizar_login(self, usuario, contra):
        """Función que se ejecuta en un hilo separado para no congelar la interfaz"""
        try:
            print(f"🔐 Intentando login para: {usuario}")
            
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                self.root.after(0, self._habilitar_botones)
                return
            
            print("✓ Conectado al servidor")
            cliente.enviar("login")
            cliente.enviar(usuario)
            cliente.enviar(contra)
            
            print("📤 Datos enviados, esperando respuesta...")
            respuesta = cliente.recibir()
            print(f"📥 Respuesta recibida: {respuesta}")
            cliente.cerrar()

            # Usar after() para actualizar la interfaz desde el hilo principal
            if respuesta and "Login Exitoso" in respuesta:
                print(f"✅ Login exitoso")
                self.usuario_actual = usuario
                self.root.after(0, self.mostrar_perfil)
            else:
                print(f"❌ Login fallido")
                self.root.after(0, lambda: messagebox.showerror("Error", "Usuario o contraseña incorrectos"))
                self.root.after(0, self._habilitar_botones)
                
        except Exception as e:
            print(f"❌ Error en login: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}"))
            self.root.after(0, self._habilitar_botones)

    def _habilitar_botones(self):
        """Habilitar botones después de un intento de login"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, tk.Frame):
                        for b in btn.winfo_children():
                            if isinstance(b, tk.Button):
                                b.config(state='normal')

    
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
            text="Foto de perfil:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(anchor='w', pady=(0, 5))

        
        frame_foto = tk.Frame(frame_form, bg=self.colores['blanco'])
        frame_foto.pack(pady=(0, 20))

        
        self.label_ruta_foto = tk.Label(
            frame_foto,
            text="Ningún archivo seleccionado",
            font=('Arial', 10),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        )
        self.label_ruta_foto.pack(side='left', padx=(0, 10))

        
        btn_seleccionar = tk.Button(
            frame_foto,
            text="Seleccionar Foto",
            font=('Arial', 10),
            bg=self.colores['gris'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.seleccionar_foto
        )
        btn_seleccionar.pack(side='left')

        
        btn_registrar = tk.Button(
            frame_form,
            text="Crear Cuenta",
            font=('Arial', 12, 'bold'),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            width=35,
            height=2,
            cursor='hand2',
            command=self.click_registrar
        )
        btn_registrar.pack(pady=(10, 5))

        
        btn_volver = tk.Button(
            frame_form,
            text="Ya tengo cuenta",
            font=('Arial', 10),
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            cursor='hand2',
            relief=tk.FLAT,
            command=self.mostrar_login
        )
        btn_volver.pack()

    
    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")]
        )
        
        if archivo:
            self.foto_perfil_path = archivo
            nombre_archivo = os.path.basename(archivo)
            self.label_ruta_foto.config(text=nombre_archivo)

    
    def click_registrar(self):
        nombre = self.entry_nombre_completo.get()
        usuario = self.entry_usuario_nuevo.get()
        password = self.entry_password_nuevo.get()
        password_confirm = self.entry_password_confirm.get()
        
        if not all([nombre, usuario, password, password_confirm]):
            messagebox.showwarning("Advertencia", "Complete todos los campos obligatorios")
            return
        
        if password != password_confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        foto = self.foto_perfil_path if self.foto_perfil_path else ""
        
        # Ejecutar registro en un hilo separado
        threading.Thread(target=self._realizar_registro, args=(usuario, nombre, password, foto), daemon=True).start()

    def _realizar_registro(self, usuario, nombre, password, foto):
        """Función que se ejecuta en un hilo separado"""
        try:
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                return
                
            cliente.enviar("registro")
            cliente.enviar(usuario)
            cliente.enviar(nombre)
            cliente.enviar(password)
            cliente.enviar(foto)
            
            respuesta = cliente.recibir()
            cliente.cerrar()
            
            if respuesta and "Registro Exitoso" in respuesta:
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Cuenta creada correctamente"))
                self.root.after(0, self.mostrar_login)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo crear la cuenta"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al registrar: {str(e)}"))

    
    # ----------PANTALLA DE PERFIL-------------
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
        
        btn_buscar = tk.Button(
            frame_top,
            text="🔍 Buscar",
            font=('Arial', 11),
            bg=self.colores['blanco'],
            fg=self.colores['texto'],
            cursor='hand2',
            command=self.mostrar_buscar
        )
        btn_buscar.pack(side='left', padx=10)
        
        btn_logout = tk.Button(
            frame_top,
            text="Cerrar Sesión",
            font=('Arial', 11),
            bg='#dc3545',
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.mostrar_login
        )
        btn_logout.pack(side='right', padx=20)
        
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True)
        
        frame_info = tk.Frame(frame_principal, bg=self.colores['blanco'], padx=40, pady=30)
        frame_info.pack(pady=20, padx=20, fill='x')
        
        tk.Label(
            frame_info,
            text=f"¡Bienvenido, {self.usuario_actual}!",
            font=('Arial', 24, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=10)
        
        frame_amigos = tk.Frame(frame_principal, bg=self.colores['blanco'], padx=20, pady=20)
        frame_amigos.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            frame_amigos,
            text="Mis Amigos",
            font=('Arial', 18, 'bold'),
            bg=self.colores['blanco']
        ).pack(pady=10)
        
        canvas_amigos = tk.Canvas(frame_amigos, bg=self.colores['blanco'])
        scrollbar_amigos = ttk.Scrollbar(frame_amigos, orient="vertical", command=canvas_amigos.yview)
        self.frame_lista_amigos = tk.Frame(canvas_amigos, bg=self.colores['blanco'])
        
        self.frame_lista_amigos.bind(
            "<Configure>",
            lambda e: canvas_amigos.configure(scrollregion=canvas_amigos.bbox("all"))
        )
        
        canvas_amigos.create_window((0, 0), window=self.frame_lista_amigos, anchor="nw")
        canvas_amigos.configure(yscrollcommand=scrollbar_amigos.set)
        
        canvas_amigos.pack(side="left", fill="both", expand=True)
        scrollbar_amigos.pack(side="right", fill="y")
        
        # Cargar amigos desde el servidor en un hilo separado
        threading.Thread(target=self.cargar_amigos, daemon=True).start()

    def cargar_amigos(self):
        """Cargar la lista de amigos desde el servidor"""
        try:
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                return
            
            cliente.enviar("obtener_amigos")
            cliente.enviar(self.usuario_actual)
            
            amigos = cliente.recibir_json()
            cliente.cerrar()
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, lambda: self._mostrar_amigos(amigos))
            
        except Exception as e:
            print(f"Error al cargar amigos: {e}")
            self.root.after(0, lambda: self._mostrar_amigos(None))

    def _mostrar_amigos(self, amigos):
        """Mostrar amigos en la interfaz (debe ejecutarse en el hilo principal)"""
        for widget in self.frame_lista_amigos.winfo_children():
            widget.destroy()
        
        if not amigos:
            tk.Label(
                self.frame_lista_amigos,
                text="No tienes amigos aún. ¡Busca personas para agregar!",
                font=('Arial', 12),
                bg=self.colores['blanco'],
                fg=self.colores['gris']
            ).pack(pady=20)
            return
        
        for amigo in amigos:
            frame_amigo = tk.Frame(
                self.frame_lista_amigos,
                bg=self.colores['fondo'],
                relief=tk.SOLID,
                borderwidth=1
            )
            frame_amigo.pack(fill='x', padx=5, pady=5)
            
            tk.Label(
                frame_amigo,
                text=f"{amigo['username']} - {amigo['nombre']}",
                font=('Arial', 12),
                bg=self.colores['fondo']
            ).pack(side='left', padx=10, pady=10)
            
            btn_ver = tk.Button(
                frame_amigo,
                text="Ver Perfil",
                font=('Arial', 9),
                bg=self.colores['primario'],
                fg=self.colores['blanco'],
                cursor='hand2',
                command=lambda a=amigo: self.click_ver_perfil_amigo(a)
            )
            btn_ver.pack(side='right', padx=5, pady=5)

    
    def click_ver_perfil_amigo(self, amigo):
        messagebox.showinfo("Ver Perfil", f"Mostrando perfil de {amigo['username']}")

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

        
        self.entry_buscar_nombre = tk.Entry(
            frame_busqueda,
            font=('Arial', 12),
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_buscar_nombre.pack(side='left', padx=(0, 20))
        
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
        """Buscar personas en el servidor"""
        nombre = self.entry_buscar_nombre.get()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese un nombre de usuario para buscar")
            return
        
        # Limpiar resultados anteriores
        for widget in self.frame_lista_resultados.winfo_children():
            widget.destroy()
        
        # Mostrar mensaje de carga
        tk.Label(
            self.frame_lista_resultados,
            text="Buscando...",
            font=('Arial', 12),
            bg=self.colores['blanco'],
            fg=self.colores['gris']
        ).pack(pady=20)

        # Ejecutar búsqueda en un hilo separado
        threading.Thread(target=self._realizar_busqueda, args=(nombre,), daemon=True).start()

    def _realizar_busqueda(self, nombre):
        """Función que se ejecuta en un hilo separado"""
        try:
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                return
            
            cliente.enviar("buscar")
            cliente.enviar(nombre)
            cliente.enviar(self.usuario_actual)
            
            resultados = cliente.recibir_json()
            cliente.cerrar()
            
            # Actualizar interfaz en el hilo principal
            self.root.after(0, lambda: self._mostrar_resultados(resultados))
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.root.after(0, lambda: self._mostrar_resultados(None))

    def _mostrar_resultados(self, resultados):
        """Mostrar resultados en la interfaz"""
        for widget in self.frame_lista_resultados.winfo_children():
            widget.destroy()
        
        if not resultados:
            tk.Label(
                self.frame_lista_resultados,
                text="No se encontraron resultados",
                font=('Arial', 12),
                bg=self.colores['blanco'],
                fg=self.colores['gris']
            ).pack(pady=20)
            return
        
        for resultado in resultados:
            self.mostrar_resultado_busqueda(resultado)


    def mostrar_resultado_busqueda(self, resultado):
        """Mostrar un resultado de búsqueda con opciones de amistad"""
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
            font=('Arial', 14, 'bold'),
            bg=self.colores['fondo']
        ).pack(side='left', padx=20, pady=15)

        
        # Si ya son amigos
        if resultado['es_amigo']:
            tk.Label(
                frame_resultado,
                text="✓ Amigo",
                font=('Arial', 11),
                bg=self.colores['fondo'],
                fg=self.colores['secundario']
            ).pack(side='right', padx=10)
            
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

        # Si no son amigos
        else:
            btn_agregar = tk.Button(
                frame_resultado,
                text="+ Agregar Amigo",
                font=('Arial', 10),
                bg=self.colores['secundario'],
                fg=self.colores['blanco'],
                cursor='hand2',
                command=lambda: self.click_agregar_amistad(resultado)
            )
            btn_agregar.pack(side='right', padx=5, pady=5)

    

    def click_eliminar_amistad(self, resultado):
        """Eliminar una amistad"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar la amistad con {resultado['username']}?"
        )
        
        if respuesta:
            threading.Thread(target=self._realizar_eliminar_amistad, args=(resultado,), daemon=True).start()

    def _realizar_eliminar_amistad(self, resultado):
        """Eliminar amistad en un hilo separado"""
        try:
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                return
            
            cliente.enviar("eliminar_amistad")
            cliente.enviar(self.usuario_actual)
            cliente.enviar(resultado['username'])
            
            respuesta_servidor = cliente.recibir()
            cliente.cerrar()
            
            if respuesta_servidor and "eliminada" in respuesta_servidor:
                self.root.after(0, lambda: messagebox.showinfo("Éxito", f"Amistad con {resultado['username']} eliminada"))
                self.root.after(0, self.click_buscar_persona)
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo eliminar la amistad"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))
            

    def click_agregar_amistad(self, resultado):
        """Enviar solicitud de amistad"""
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Desea enviar solicitud de amistad a {resultado['username']}?"
        )

        if respuesta:
            threading.Thread(target=self._realizar_solicitud_amistad, args=(resultado,), daemon=True).start()


    def _realizar_solicitud_amistad(self, resultado):
        """Enviar solicitud en un hilo separado"""
        try:
            cliente = ClienteTCP()
            if not cliente.conectar(ip, puerto):
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo conectar al servidor"))
                return
            
            cliente.enviar("solicitar_amistad")
            cliente.enviar(self.usuario_actual)
            cliente.enviar(resultado['username'])
            
            respuesta_servidor = cliente.recibir()
            cliente.cerrar()
            
            if respuesta_servidor and "enviada" in respuesta_servidor:
                self.root.after(0, lambda: messagebox.showinfo("Éxito", f"Solicitud enviada a {resultado['username']}"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo enviar la solicitud"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {str(e)}"))




    


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialtecCliente(root)
    root.mainloop()