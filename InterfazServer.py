import tkinter as tk
from tkinter import messagebox
import json
from Grafo import Grafo   
from Base_de_datos import BaseDeDatos
from Cliente_Prueba import ClienteTCP

IP = "127.0.0.1"
PUERTO = 5001

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Red Social")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f2f5')

        self.grafo = Grafo() 
        self.base_datos = BaseDeDatos()
        
        # Título
        tk.Label(
            root,
            text="Panel de Administración",
            font=('Arial', 24, 'bold'),
            bg='#f0f2f5',
            fg='#1877f2'
        ).pack(pady=20)
        
        # Frame para botones principales
        frame_botones = tk.Frame(root, bg='#f0f2f5')
        frame_botones.pack(pady=10)
        
        # Botón para actualizar grafo
        tk.Button(
            frame_botones,
            text="🔄 Actualizar Grafo",
            font=('Arial', 12),
            bg='#42b72a',
            fg='white',
            width=20,
            height=2,
            command=self.actualizar_grafo
        ).pack(pady=5)
        
        # Botón para imprimir grafo
        tk.Button(
            frame_botones,
            text="📊 Imprimir Grafo",
            font=('Arial', 12),
            bg='#1877f2',
            fg='white',
            width=20,
            height=2,
            command=self.imprimir_grafo
        ).pack(pady=5)

        # Sección para buscar path
        frame_path = tk.Frame(root, bg='white', padx=20, pady=20)
        frame_path.pack(pady=20, padx=20, fill='x')
        
        tk.Label(
            frame_path,
            text="Buscar Path de Amigos",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack()

        tk.Label(frame_path, text="Usuario Origen:", bg='white').pack(pady=(10, 0))
        self.entry_origen = tk.Entry(frame_path, font=('Arial', 11), width=30)
        self.entry_origen.pack(pady=5)

        tk.Label(frame_path, text="Usuario Destino:", bg='white').pack(pady=(10, 0))
        self.entry_destino = tk.Entry(frame_path, font=('Arial', 11), width=30)
        self.entry_destino.pack(pady=5)

        tk.Button(
            frame_path,
            text="🔍 Buscar Path",
            font=('Arial', 11),
            bg='#1877f2',
            fg='white',
            command=self.buscar_path
        ).pack(pady=10)

        self.resultado_path = tk.Label(
            frame_path,
            text="",
            font=('Arial', 10),
            bg='white',
            fg='#42b72a',
            wraplength=400
        )
        self.resultado_path.pack(pady=5)

        # Sección de estadísticas
        frame_stats = tk.Frame(root, bg='white', padx=20, pady=20)
        frame_stats.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Button(
            frame_stats,
            text="📈 Mostrar Estadísticas",
            font=('Arial', 12),
            bg='#1877f2',
            fg='white',
            command=self.mostrar_estadisticas
        ).pack(pady=10)

        self.stats_label = tk.Label(
            frame_stats,
            text="",
            font=('Arial', 11),
            bg='white',
            justify="left"
        )
        self.stats_label.pack(pady=10)
        
        # Cargar el grafo al inicio
        self.actualizar_grafo()

    def actualizar_grafo(self):
        """Actualiza el grafo desde la base de datos"""
        try:
            # Obtener todas las amistades de la base de datos
            amistades = self.base_datos.obtener_todas_las_amistades()
            
            # Reconstruir el grafo
            self.grafo.construir_desde_bd(amistades)
            
            messagebox.showinfo(
                "Éxito",
                f"Grafo actualizado con {len(amistades)} amistades"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar grafo: {e}")

    def imprimir_grafo(self):
        """Imprime el grafo visualmente"""
        try:
            if not self.grafo.grafo:
                messagebox.showwarning(
                    "Advertencia",
                    "El grafo está vacío. Actualice el grafo primero."
                )
                return
            
            self.grafo.imprimir_grafo()
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir grafo: {e}")

    def buscar_path(self):
        """Busca un camino entre dos usuarios"""
        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()
        
        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Ingrese ambos usuarios")
            return
        
        # Verificar que los usuarios existan en el grafo
        if origen not in self.grafo.grafo:
            self.resultado_path.config(
                text=f"El usuario '{origen}' no existe en el grafo",
                fg='red'
            )
            return
        
        if destino not in self.grafo.grafo:
            self.resultado_path.config(
                text=f"El usuario '{destino}' no existe en el grafo",
                fg='red'
            )
            return

        # Buscar el path
        existe, path = self.grafo.existe_path(origen, destino)

        if existe:
            self.resultado_path.config(
                text=f"✓ Sí existe path:\n{' → '.join(path)}",
                fg='#42b72a'
            )
        else:
            self.resultado_path.config(
                text="✗ No existe path entre los usuarios",
                fg='red'
            )

    def mostrar_estadisticas(self):
        """Muestra estadísticas de la red social"""
        try:
            mas = self.base_datos.usuario_con_mas_amigos()
            menos = self.base_datos.usuario_con_menos_amigos()
            promedio = self.base_datos.promedio_amigos()

            texto = (
                f"📊 Estadísticas de la Red\n\n"
                f"Usuario con más amigos: {mas[0]} ({mas[1]} amigos)\n\n"
                f"Usuario con menos amigos: {menos[0]} ({menos[1]} amigos)\n\n"
                f"Promedio de amigos: {promedio:.2f}"
            )

            self.stats_label.config(text=texto)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()