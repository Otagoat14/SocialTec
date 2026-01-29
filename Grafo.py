import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.grafo = {}

    def crear_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = set()

        else:
            print("El usuario ya existe")


    def apuntar(self, origen, destino):
        if origen not in self.grafo or destino not in self.grafo:
            print("Uno de los usuarios no existe")
            return

        if origen == destino:
            print("El usuario no puede hacerse amigo de si mismo")
            return

        self.grafo[origen].add(destino)
        self.grafo[destino].add(origen)

           

    def buscar_usuario(self, usuario):
        if usuario in self.grafo:
            return usuario in self.grafo

        else:
            print("El usuario no existe")
            


    def obtener_amigos(self, usuario):
        if usuario in self.grafo:
            return self.grafo[usuario]
        

    def eliminar_amistad(self, origen, destino):
        if origen not in self.grafo:
            print("No existe un usuario con amigos que eliminar")
        
        elif destino not in self.grafo:
            print(" El usuario a eliminar no existe")

        elif destino not in self.grafo[origen]:
            print(f"El usuario no es amigo de {destino}")

        else:
            self.grafo[origen].remove(destino)
            self.grafo[destino].remove(origen)

    def imprimir_grafo(self):
        G = nx.Graph()

        for usuario, amigos in self.grafo.items():
            for amigo in amigos:
                G.add_edge(usuario, amigo)

        nx.draw(G, with_labels=True)
        plt.show()

        

grafo = Grafo()


grafo.crear_nodo("Juan")
grafo.crear_nodo("Andres")
grafo.crear_nodo("Carlos")
grafo.crear_nodo("Daniel")

grafo.apuntar("Juan", "Carlos")
grafo.apuntar("Juan", "Andres")
grafo.apuntar("Juan", "Daniel")
grafo.apuntar("Andres", "Carlos")
grafo.apuntar("Andres", "Daniel")
grafo.apuntar("Andres", "Juan")
grafo.apuntar("Daniel", "Carlos")

print(grafo.grafo)

grafo.imprimir_grafo()
grafo.buscar_usuario("Juan")

#grafo.obtener_amigos("Juan")

        



