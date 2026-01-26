import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from Registro import ManejoUsuarios


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

        if self.registro.login(usuario, contra):
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
        
        
        self.registro.registrar_usuario(usuario, contra, nombre_completo, self.foto_perfil_path)
        messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
        self.mostrar_login()

    #PERFILES Y AMIGOS
    def mostrar_perfil(self):
        messagebox.showinfo("HOLI")
    


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialtecCliente(root)
    root.mainloop()
    
    