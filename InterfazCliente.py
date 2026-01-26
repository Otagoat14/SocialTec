import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os


class SocialtecCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Socialtec - Red Social")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.usuario_actual = None
        self.foto_perfil_path = None
        self.configurar_estilo()
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
    
    