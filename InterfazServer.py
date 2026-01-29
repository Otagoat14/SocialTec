import tkinter as tk
from tkinter import messagebox
from Grafo import Grafo   
from Base_de_datos import BaseDeDatos

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Red Social")

        self.grafo = Grafo() 
        self.base_datos = BaseDeDatos()
        # -------- SECCIÓN GRAFO --------
        tk.Button(root, text="Imprimir Grafo", command=self.imprimir_grafo).pack(pady=5)

        # -------- SECCIÓN PATH --------
        tk.Label(root, text="Buscar Path de Amigos").pack()

        self.entry_origen = tk.Entry(root)
        self.entry_origen.pack()
        self.entry_origen.insert(0, "Usuario A")

        self.entry_destino = tk.Entry(root)
        self.entry_destino.pack()
        self.entry_destino.insert(0, "Usuario D")

        tk.Button(root, text="Buscar Path", command=self.buscar_path).pack(pady=5)

        self.resultado_path = tk.Label(root, text="")
        self.resultado_path.pack()

        # -------- SECCION ESTADISTICAS --------
        tk.Button(root, text="Mostrar Estadísticas", command=self.mostrar_estadisticas).pack(pady=10)

        self.stats_label = tk.Label(root, text="", justify="left")
        self.stats_label.pack()

    # -------- FUNCIONES --------

    def imprimir_grafo(self):
        self.grafo.imprimir_grafo()

    def buscar_path(self):
        origen = self.entry_origen.get()
        destino = self.entry_destino.get()

        existe, path = self.grafo.existe_path(origen, destino)

        if existe:
            self.resultado_path.config(
                text=f"Sí existe path:\n{' → '.join(path)}"
            )
        else:
            self.resultado_path.config(text="No existe path entre los usuarios")


    def mostrar_estadisticas(self):
        mas = self.base_datos.usuario_con_mas_amigos()
        menos = self.base_datos.usuario_con_menos_amigos()
        promedio = self.base_datos.promedio_amigos()

        texto = (
            f"Usuario con más amigos: {mas}\n"
            f"Usuario con menos amigos: {menos}\n"
            f"Promedio de amigos: {promedio:.2f}"
        )

        self.stats_label.config(text=texto)

if __name__ == "__main__":

    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()

