import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from Registro import ManejoUsuarios

#CREO QUE HAY UN PROBLEMA CON LA LOGICA YA QUE EL SERVIDOR DEBERIA HACER TODAS LAS OPERACIONES HABRIA QUE HACERLAS EN EL SERVIDOR
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

        #ESTO TAMBIEN HAY QUE CAMBIARLO CON LA LOGICA DEL SERVIDOR
<<<<<<< HEAD
        if self.registro.login(usuario, contra) == True:
=======
        if self.registro.login(usuario, contra):
>>>>>>> d059e9bcf077a9a26bfd10513af49c421b2dcf0d
            self.usuario_actual = usuario
            self.mostrar_perfil()

    
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

        
        self.label_foto = tk.Label(
            frame_foto,
            text="Sin foto seleccionada",
            font=('Arial', 10),
            bg=self.colores['fondo'],
            width=30,
            height=2
        )
        self.label_foto.pack(side='left', padx=(0, 10))

        
        btn_foto = tk.Button(
            frame_foto,
            text="Seleccionar",
            font=('Arial', 10),
            bg=self.colores['primario'],
            fg=self.colores['blanco'],
            cursor='hand2',
            command=self.seleccionar_foto
        )
        btn_foto.pack(side='left')
        
        
        frame_botones = tk.Frame(frame_form, bg=self.colores['blanco'])
        frame_botones.pack(pady=10)
        
        
        btn_crear = tk.Button(
            frame_botones,
            text="Crear Cuenta",
            font=('Arial', 12, 'bold'),
            bg=self.colores['secundario'],
            fg=self.colores['blanco'],
            width=15,
            height=2,
            cursor='hand2',
            command=self.click_crear_cuenta
        )
        btn_crear.pack(side='left', padx=5)

        
        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            font=('Arial', 12),
            bg=self.colores['gris'],
            fg=self.colores['blanco'],
            width=15,
            height=2,
            cursor='hand2',
            command=self.mostrar_login
        )
        btn_cancelar.pack(side='left', padx=5)

    
    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if archivo:
            self.foto_perfil_path = archivo
            nombre_archivo = os.path.basename(archivo)
            self.label_foto.config(text=nombre_archivo)

    
    def click_crear_cuenta(self):
        #AQUI TODAVIA NO HE PEGADO LA LOGICA JUNTO CON LA PARTE DE feature/Cliente
        nombre_completo = self.entry_nombre_completo.get()
        usuario = self.entry_usuario_nuevo.get()
        contra = self.entry_password_nuevo.get()
        contra_confirmacion = self.entry_password_confirm.get()
        
        
        if not all([nombre_completo, usuario, contra, contra_confirmacion]):
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
            return
        
        if contra != contra_confirmacion:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if not self.foto_perfil_path:
            messagebox.showwarning("Advertencia", "Por favor seleccione una foto de perfil")
            return
        
        #AQUI NO SERIA REGISTRARLO DE UNA VEZ SINO MANDARLO AL ERVER Y DE AHI HACER LA VERIFICACION Y LLAMAR AL METODO
        self.registro.registrar_usuario(usuario, contra, nombre_completo, self.foto_perfil_path)
        messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
        self.mostrar_login()

    
    #---------PAGINA PERFIL---------------  
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
            text="Buscar Personas",
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
            text="Perfil de usuario",
            font=('Arial', 12),
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
        
        
    #ESTA FUNCION SE REMPLAZARA EN BASE A LA LOGICA CON QUE SE CREEN LOS AMIGOS
    def mostrar_lista_amigos_ejemplo(self):

        amigos_ejemplo = [
            "Ana García",
            "Carlos Rodríguez",
            "Elena Martínez",
            "Juan Pérez",
            "María López"
        ]

        
        for amigo in amigos_ejemplo:
            frame_amigo = tk.Frame(
                self.frame_lista_amigos,
                bg=self.colores['fondo'],
                relief=tk.SOLID,
                borderwidth=1
            )
            frame_amigo.pack(fill='x', padx=5, pady=5)
            

            tk.Label(
                frame_amigo,
                text=amigo,
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

    
    def click_ver_perfil_amigo(self, nombre_amigo):
        messagebox.showinfo("Ver Perfil", f"Mostrando perfil de {nombre_amigo}")

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
            text="Nombre:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(side='left', padx=(0, 10))

        
        self.entry_buscar_nombre = tk.Entry(
            frame_busqueda,
            font=('Arial', 12),
            width=20,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_buscar_nombre.pack(side='left', padx=(0, 20))
        
        
        tk.Label(
            frame_busqueda,
            text="Apellido:",
            font=('Arial', 12),
            bg=self.colores['blanco']
        ).pack(side='left', padx=(0, 10))

        
        self.entry_buscar_apellido = tk.Entry(
            frame_busqueda,
            font=('Arial', 12),
            width=20,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.entry_buscar_apellido.pack(side='left', padx=(0, 20))
        
        
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
        
        nombre = self.entry_buscar_nombre.get()
        apellido = self.entry_buscar_apellido.get()
        
        
        if not nombre and not apellido:
            messagebox.showwarning("Advertencia", "Ingrese al menos un criterio de búsqueda")
            return
        
        
        for widget in self.frame_lista_resultados.winfo_children():
            widget.destroy()
        
        
        resultados_ejemplo = [
            {"nombre": "Juan Pérez", "es_amigo": True},
            {"nombre": "María Pérez", "es_amigo": False},
            {"nombre": "Pedro Pérez", "es_amigo": False}
        ]
        
        
        for resultado in resultados_ejemplo:
            self.mostrar_resultado_busqueda(resultado)


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
            text=resultado['nombre'],
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
            command=lambda: self.click_ver_perfil_busqueda(resultado)
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
    

    def click_ver_perfil_busqueda(self, resultado):
        messagebox.showinfo("Ver Perfil", f"Mostrando perfil de {resultado['nombre']}")
    

    def click_eliminar_amistad(self, resultado):
        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar la amistad con {resultado['nombre']}?"
        )
        
        #AQUI NO HAY NINGUNA LOIGICA DE AMIGOS IMPLEMENTAD AUN
        if respuesta:
            messagebox.showinfo("Éxito", f"Amistad con {resultado['nombre']} eliminada")
            self.click_buscar_persona()  




    


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialtecCliente(root)
    root.mainloop()
    
    