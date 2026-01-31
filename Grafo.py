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

    def existe_path(self, inicio, fin):
        visitados = set()
        path = []

        def dfs(actual):
            visitados.add(actual)
            path.append(actual)

            if actual == fin:
                return True

            for vecino in self.grafo.get(actual, []):
                if vecino not in visitados:
                    if dfs(vecino):
                        return True

            path.pop()
            return False

        existe = dfs(inicio)
        return existe, path if existe else []
    
    def construir_desde_bd(self, lista_amistades):
        self.grafo.clear()

        for usuario, amigo in lista_amistades:
            if usuario not in self.grafo:
                self.crear_nodo(usuario)
            if amigo not in self.grafo:
                self.crear_nodo(amigo)

            self.apuntar(usuario, amigo)



        


